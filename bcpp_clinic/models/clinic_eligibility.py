from uuid import uuid4
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models

from django_crypto_fields.fields import FirstnameField
from edc_constants.choices import YES_NO_UNKNOWN, GENDER, YES_NO_NA, YES_NO
from edc_constants.constants import NOT_APPLICABLE

from .clinic_consent import ClinicConsent
from .clinic_enrollment_loss import ClinicEnrollmentLoss
from .clinic_household_member import ClinicHouseholdMember
from member.models.household_member.household_member import HouseholdMember
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from survey.model_mixins import SurveyScheduleModelMixin
from edc_base.utils import get_utcnow
from member.choices import INABILITY_TO_PARTICIPATE_REASON
from bcpp_clinic.choices import VERBALHIVRESULT_CHOICE
from edc_map.site_mappers import site_mappers
from household.models.household_structure.household_structure import HouseholdStructure
from survey.site_surveys import site_surveys
from bcpp_clinic.constants import CLINIC_RBD
from edc_base.model_validators.date import datetime_not_future
from edc_base.model_validators.dob import dob_not_future
from edc_consent.field_mixins.bw.identity_fields_mixin import IdentityFieldsMixin
from edc_base.model_managers.historical_records import HistoricalRecords
from bcpp_clinic.models.clinic_refused_member import ClinicRefusedMember


class ClinicEligibility (IdentityFieldsMixin, SurveyScheduleModelMixin, BaseUuidModel):
    """A model completed by the user that confirms and saves eligibility
    information for potential participant."""

    household_member = models.OneToOneField(
        HouseholdMember, on_delete=models.PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name='Report date',
        default=get_utcnow,
        validators=[datetime_not_future])

    first_name = FirstnameField(
        verbose_name='First name',
        validators=[RegexValidator("^[A-Z]{1,250}$", "Ensure first name is in CAPS and "
                                   "does not contain any spaces or numbers")],
        help_text="")

    initials = models.CharField(
        verbose_name='Initials',
        max_length=3,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3),
            RegexValidator("^[A-Z]{1,3}$", "Must be Only CAPS and 2 or 3 letters. No spaces or numbers allowed.")],
        help_text="")

    dob = models.DateField(
        verbose_name="Date of birth",
        validators=[dob_not_future, ],
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD.")

    verbal_age = models.IntegerField(
        verbose_name='Age in years as reported by patient',
        null=True,
        blank=True,
        help_text='Complete if DOB is not provided, otherwise leave BLANK.')

    guardian = models.CharField(
        verbose_name="If minor, is there a guardian available? ",
        max_length=10,
        choices=YES_NO_NA,
        help_text="If a minor age 16 and 17, ensure a guardian is available otherwise"
                  " participant will not be enrolled.")

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER)

    has_identity = models.CharField(
        verbose_name="[Interviewer] Has the subject presented a valid OMANG or other identity document?",
        max_length=10,
        choices=YES_NO,
        help_text='Allow Omang, Passport number, driver\'s license number or Omang receipt number. '
                  'If \'NO\' participant will not be enrolled.')

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text="")

    legal_marriage = models.CharField(
        verbose_name="If not a citizen, are you legally married to a Botswana Citizen?",
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If 'NO' participant is not eligible.")

    marriage_certificate = models.CharField(
        verbose_name=("[Interviewer] Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If 'NO' participant is not eligible.")

    part_time_resident = models.CharField(
        verbose_name="In the past 12 months, have you typically spent 3 or"
                     " more nights per month in this community? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text=(
            "If participant has moved into the "
            "community in the past 12 months, then "
            "since moving in has the participant typically "
            "spent more than 3 nights per month in this community. "
            "If 'NO (or don't want to answer)' STOP. Participant is not eligible."),
    )

    literacy = models.CharField(
        verbose_name="Is the participant LITERATE?, or if ILLITERATE, is there a"
                     "  LITERATE witness available ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text="If participate is illiterate, confirm there is a literate"
                  "witness available otherwise participant is not eligible.")

    inability_to_participate = models.CharField(
        verbose_name="Do any of the following reasons apply to the participant?",
        max_length=17,
        choices=INABILITY_TO_PARTICIPATE_REASON,
        help_text=("Participant can only participate if NONE is selected. "
                   "(Any of these reasons make the participant unable to take "
                   "part in the informed consent process)"),
    )

    hiv_status = models.CharField(
        verbose_name="Please tell me your current HIV status?",
        max_length=30,
        choices=VERBALHIVRESULT_CHOICE,
        help_text='If not HIV(+) participant is not elgiible.'
    )

    age_in_years = models.IntegerField(editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    is_consented = models.BooleanField(
        default=False,
        editable=False)

    is_refused = models.BooleanField(
        default=False,
        editable=False)

    loss_reason = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        null=True,
        editable=False,
        help_text='(stored for the loss form)')

    consent_datetime = models.DateTimeField(
        editable=False,
        null=True,
        help_text='filled from clinic_consent'
    )

    community = models.CharField(max_length=25, editable=False)

    additional_key = models.CharField(
        max_length=36,
        verbose_name='-',
        editable=False,
        default=None,
        null=True,
        help_text=('A uuid to be added to clinic members to bypass the '
                   'unique constraint for firstname, initials, household_structure. '
                   'Always null for non-clinic members.'),
    )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        if 'is_consented' in update_fields or 'is_refused' in update_fields:
            pass
        else:
            if not self.identity:
                self.additional_key = uuid4()
            else:
                self.additional_key = None
            self.check_for_consent(self.identity)
            if self.identity:
                if not self.id:
                    self.check_for_known_identity(self.identity)
            self.age_in_years = relativedelta(self.report_datetime.date(), self.dob).years
            self.is_eligible, self.loss_reason = self.passes_enrollment_criteria()
            self.community = site_mappers.current_map_area
            if not self.household_member:
                self.household_member = self.clinic_household_member
        super(ClinicEligibility, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({}) {}/{}".format(
            self.first_name, self.initials, self.gender, self.age_in_years)

    @property
    def clinic_household_member(self):
        """Returns the household_member and will create if one does not exist.

        ClinicHouseholdMember is a proxy model of HouseholdMember."""
        try:
            clinic_household_member = ClinicHouseholdMember.objects.get(pk=self.household_member.pk)
        except (ClinicHouseholdMember.DoesNotExist, AttributeError):
            schedule_name = site_surveys.get_survey_schedules(current=True)[0]
            try:
                household_structure = HouseholdStructure.objects.get(
                    household__plot=site_mappers.current_mapper().clinic_plot,
                    survey_schedule=schedule_name)
            except HouseholdStructure.DoesNotExist:
                raise ValidationError(f'Missing household structure for survey schedule {schedule_name}')
            else:
                clinic_household_member = ClinicHouseholdMember.objects.create(
                    household_structure=household_structure,
                    first_name=self.first_name,
                    initials=self.initials,
                    age_in_years=self.age_in_years,
                    gender=self.gender,
                    present_today='N/A',
                    inability_to_participate=self.inability_to_participate,
                    study_resident=self.part_time_resident,
                    member_status=CLINIC_RBD,
                    is_consented=False,
                    relation='UNKNOWN',
                    eligible_member=True,
                    eligible_subject=True,
                    additional_key=self.additional_key)

        if not self.household_member:
            # only set if self.household_member was None
            self.household_member = clinic_household_member
        return self.household_member

    @classmethod
    def check_for_consent(cls, identity, exception_cls=None):
        """Confirms subject with this identity has not previously consented."""
        SubjectConsent = models.get_model('bcpp_clinic', 'SubjectConsent')
        exception_cls = exception_cls or ValidationError
        clinic_consent = None
        try:
            clinic_consent = ClinicConsent.objects.get(identity=identity)
            raise exception_cls('Subject was consented as {} on {}. '
                                'Eligibility checklist may not be edited.'.format(
                                    clinic_consent.subject_identifier,
                                    clinic_consent.consent_datetime))
        except ClinicConsent.DoesNotExist:
            pass
        try:
            subject_consent = SubjectConsent.objects.get(identity=identity)
            raise exception_cls(
                'A Household member was consented during BHS with study identifier {} on {}. '
                'Eligibility checklist may not be completed for personal identifier {}.'.format(
                    subject_consent.subject_identifier,
                    subject_consent.modified,
                    subject_consent.identity))
        except SubjectConsent.DoesNotExist:
            pass
        except SubjectConsent.MultipleObjectsReturned:
            pass
        return None

    def passes_enrollment_criteria(self):
        """Creates or updates (or deletes) the enrollment loss based on the
        reason for not passing the enrollment checklist."""
        loss_reason = []
        if self.age_in_years < 16:
            loss_reason.append('Too young (<16).')
        if self.age_in_years > 64:
            loss_reason.append('Too old (>64).')
        if self.has_identity == 'No' or not self.identity:
            loss_reason.append('No valid identity.')
        if self.part_time_resident == 'No':
            loss_reason.append('Not resident.')
        if self.part_time_resident == 'Unknown':
            loss_reason.append('Residency unknown.')
        if self.citizen == 'No' and self.legal_marriage == 'No':
            loss_reason.append('Not a citizen and not married to a citizen.')
        if (self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'yes' and
                self.marriage_certificate == 'No'):
            loss_reason.append('Not a citizen, married to a citizen but does not have a marriage certificate.')
        if self.literacy == 'No':
            loss_reason.append('Illiterate with no literate witness.')
        if self.literacy == 'Unknown':
            loss_reason.append('Literacy unknown.')
        if self.age_in_years < 18 and self.guardian != 'Yes':
            loss_reason.append('Minor without guardian available.')
        if self.inability_to_participate != 'N/A':
            loss_reason.append('Mental Incapacity/Deaf/Mute/Too sick.')
        if self.hiv_status == 'NEG':
            loss_reason.append('HIV Negative.')
        if self.hiv_status != 'POS' and self.hiv_status != 'NEG':
            loss_reason.append('HIV status unknown.')
        if not self.identity:
            loss_reason.append('Identity unknown.')
        if not self.dob:
            loss_reason.append('DOB unknown.')
        if not self.citizen:
            loss_reason.append('Citizenship unknown.')
        return (False if loss_reason else True, loss_reason)

    @property
    def reason_ineligible(self):
        reason = []
        if self.age_in_years < 16:
            reason.append('Minor.')
        if self.age_in_years > 64:
            reason.append('Too old.')
        if self.part_time_resident == 'No':
            reason.append('Not resident.')
        if self.part_time_resident == 'Unknown':
            reason.append('Residency unknown.')
        if self.legal_marriage == 'No':
            reason.append('Not a citizen and not married to a citizen.')
        if self.inability_to_participate:
            reason.append('Mental Incapacity/Deaf/Mute/Too sick.')
        if self.hiv_status == 'NEG':
            reason.append('HIV Negative.')
        if self.hiv_status != 'POS' and self.hiv_status != 'NEG':
            reason.append('HIV status unknown.')
        if not self.identity:
            reason.append('Identity unknown.')
        if not self.dob:
            reason.append('DOB unknown.')
        if not self.citizen:
            reason.append('Citizenship unknown.')
        reason.sort()
        return '; '.join(reason)

    @property
    def clinic_refusal(self):
        try:
            clinic_refusal = ClinicRefusedMember.objects.get(household_member=self.household_member)
        except ClinicRefusedMember.DoesNotExist:
            clinic_refusal = None
        return clinic_refusal

    @property
    def clinic_consent(self):
        try:
            clinic_consent = ClinicConsent.objects.get(household_member=self.household_member)
        except ClinicRefusedMember.DoesNotExist:
            clinic_consent = None
        return clinic_consent

    @property
    def clinic_enrollment_loss(self):
        try:
            clinic_enrollment_loss = ClinicEnrollmentLoss.objects.get(
                household_member=self.household_member)
        except ClinicEnrollmentLoss.DoesNotExist:
            clinic_enrollment_loss = None
        return clinic_enrollment_loss

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Eligibility"
        verbose_name_plural = "Clinic Eligibility"
        unique_together = ['first_name', 'initials', 'identity', 'additional_key']
