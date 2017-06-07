import re

from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models

from django_crypto_fields.fields.firstname_field import FirstnameField

from edc_base.model_managers.historical_records import HistoricalRecords
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_base.model_validators.dob import dob_not_future
from edc_base.utils import get_utcnow
from edc_constants.constants import UUID_PATTERN
from edc_consent.field_mixins.bw.identity_fields_mixin import IdentityFieldsMixin
from edc_constants.choices import YES_NO_UNKNOWN, GENDER, YES_NO_NA, YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin

from ..choices import VERBALHIVRESULT_CHOICE, INABILITY_TO_PARTICIPATE_REASON


class EligibilityIdentifierModelMixin(NonUniqueSubjectIdentifierModelMixin, models.Model):

    def update_subject_identifier_on_save(self):
        """Overridden to not set the subject identifier on save.
        """
        if not self.subject_identifier:
            self.subject_identifier = self.subject_identifier_as_pk.hex
        elif re.match(UUID_PATTERN, self.subject_identifier):
            pass
        return self.subject_identifier

    def make_new_identifier(self):
        return self.subject_identifier_as_pk.hex

    class Meta:
        abstract = True


class ClinicEligibility (EligibilityIdentifierModelMixin, IdentityFieldsMixin, BaseUuidModel):
    """A model completed by the user that confirms and saves eligibility
    information for potential participant."""

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
        verbose_name=(
            "[Interviewer] Has the participant produced the marriage certificate, as proof? "),
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
        super(ClinicEligibility, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({}) {}/{}".format(
            self.first_name, self.initials, self.gender, self.age_in_years)

    @property
    def test_property(self):
        return "This thing works cool"

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Eligibility"
        verbose_name_plural = "Clinic Eligibility"
        unique_together = [
            'first_name', 'initials', 'identity', 'additional_key']
