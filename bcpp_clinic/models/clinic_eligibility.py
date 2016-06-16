from uuid import uuid4
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin
from simple_history.models import HistoricalRecords as AuditTrail
from edc_base.encrypted_fields import FirstnameField
from edc_base.encrypted_fields import IdentityField
from edc_base.encrypted_fields import IdentityTypeField
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future)
from edc_base.model.validators import dob_not_future
from edc_constants.choices import YES_NO_UNKNOWN, GENDER, YES_NO_NA, YES_NO
from edc_constants.constants import NOT_APPLICABLE

# from ..managers import BaseClinicHouseholdMemberManager

from .clinic_consent import ClinicConsent
# from ..contants import CLINIC_RBD
from ..choices import INABILITY_TO_PARTICIPATE_REASON, VERBALHIVRESULT_CHOICE
from .clinic_enrollment_loss import ClinicEnrollmentLoss
from registration.models import RegisteredSubject
from .clinic_refusal import ClinicRefusal


class ClinicEligibility (SyncModelMixin, BaseUuidModel):
    """A model completed by the user that confirms and saves eligibility
    information for potential participant."""

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of collection'
    )

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

    identity = IdentityField(
        verbose_name="Identity number (OMANG, etc)",
        null=True,
        blank=True,
        help_text=("Use Omang, Passport number, driver's license number or Omang receipt number")
    )

    identity_type = IdentityTypeField(
        null=True)

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
        help_text=("Participant can only participate if 'ABLE to participate' is selected. "
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

#     objects = BaseClinicHouseholdMemberManager()

    history = AuditTrail()

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
        super(ClinicEligibility, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} ({}) {}/{}".format(self.first_name, self.initials, self.gender, self.age_in_years)

    @classmethod
    def check_for_known_identity(cls, identity, exception_cls=None):
        """Checks if identity number is known to RegisteredSubject and raises an error if found."""
        exception_cls = exception_cls or ValidationError
        try:
            registered_subject = RegisteredSubject.objects.get(identity=identity)
            raise exception_cls(
                'A subject with this OMANG is already registered. See Registered Subject {} {}'.format(
                    registered_subject,
                    registered_subject.subject_identifier,
                )
            )
        except RegisteredSubject.DoesNotExist:
            pass

    def natural_key(self):
        return self.registered_subject.natural_key()
    natural_key.dependencies = ['edc_registration.registered_subject', ]

    def get_registered_subject(self):
        return self.register_subject

    @classmethod
    def check_for_consent(cls, identity, exception_cls=None):
        """Confirms subject with this identity has not previously consented."""
        SubjectConsent = models.get_model('bcpp_subject', 'SubjectConsent')
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

    def age_reason(self, loss_reason):
        if self.age_in_years < 16:
            loss_reason.append('Too young (<16).')
        if self.age_in_years > 64:
            loss_reason.append('Too old (>64).')
        return loss_reason

    def literacy_reason(self, loss_reason):
        if self.literacy == 'No':
            loss_reason.append('Illiterate with no literate witness.')
        if self.literacy == 'Unknown':
            loss_reason.append('Literacy unknown.')
        return loss_reason

    def hiv_status_reason(self, loss_reason):
        if self.hiv_status == 'NEG':
            loss_reason.append('HIV Negative.')
        if self.hiv_status != 'POS' and self.hiv_status != 'NEG':
            loss_reason.append('HIV status unknown.')
        return loss_reason

    def part_time_resident_reason(self, loss_reason):
        if self.part_time_resident == 'No':
            loss_reason.append('Not resident.')
        if self.part_time_resident == 'Unknown':
            loss_reason.append('Residency unknown.')
        return loss_reason

    def passes_enrollment_criteria(self):
        """Creates or updates (or deletes) the enrollment loss based on the
        reason for not passing the enrollment checklist."""
        loss_reason = []
        loss_reason = self.age_reason(loss_reason)
        if self.has_identity == 'No' or not self.identity:
            loss_reason.append('No valid identity.')
        loss_reason = self.part_time_resident_reason(loss_reason)
        if self.citizen == 'No' and self.legal_marriage == 'No':
            loss_reason.append('Not a citizen and not married to a citizen.')
        if (self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'yes' and
                self.marriage_certificate == 'No'):
            loss_reason.append('Not a citizen, married to a citizen but does not have a marriage certificate.')
        loss_reason = self.literacy_reason(loss_reason)
        if self.age_in_years < 18 and self.guardian != 'Yes':
            loss_reason.append('Minor without guardian available.')
        if self.inability_to_participate != 'N/A':
            loss_reason.append('Mental Incapacity/Deaf/Mute/Too sick.')
        loss_reason = self.hiv_status_reason(loss_reason)
        if not self.identity:
            loss_reason.append('Identity unknown.')
        if not self.dob:
            loss_reason.append('DOB unknown.')
        if not self.citizen:
            loss_reason.append('Citizenship unknown.')
        return (False if loss_reason else True, loss_reason)

    def age_reason_ineligible(self, reason):
        if self.age_in_years < 16:
            reason.append('Minor.')
        if self.age_in_years > 64:
            reason.append('Too old.')
        return reason

    def reason_ineligible(self):
        reason = []
        reason = self.age_reason_ineligible(reason)
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
            clinic_refusal = ClinicRefusal.objects.get(registered_subject=self.registered_subject)
        except ClinicRefusal.DoesNotExist:
            clinic_refusal = None
        return clinic_refusal

    @property
    def clinic_consent(self):
        try:
            clinic_consent = ClinicConsent.objects.get(registered_subject=self.registered_subject)
        except ClinicRefusal.DoesNotExist:
            clinic_consent = None
        return clinic_consent

    @property
    def clinic_enrollment_loss(self):
        try:
            clinic_enrollment_loss = ClinicEnrollmentLoss.objects.get(registered_subject=self.registered_subject)
        except ClinicEnrollmentLoss.DoesNotExist:
            clinic_enrollment_loss = None
        return clinic_enrollment_loss

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Eligibility"
        verbose_name_plural = "Clinic Eligibility"
        unique_together = ['first_name', 'initials', 'identity', 'additional_key']
