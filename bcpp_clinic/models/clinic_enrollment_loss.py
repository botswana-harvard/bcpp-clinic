from django.db import models

from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_base.model_validators.date import datetime_not_future

from .clinic_eligibility import ClinicEligibility


class ClinicEnrollmentLoss(BaseUuidModel):
    """A system model auto created that captures the reason for a present BHS eligible member
    who passes BHS eligibility but is not participating in the BHS."""

    clinic_eligibility = models.OneToOneField(
        ClinicEligibility, on_delete=models.PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name='Report date',
        default=get_utcnow,
        validators=[datetime_not_future])

    reason = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Do not include any personal identifiable information.')

    history = HistoricalRecords()

    def natural_key(self):
        return (self.report_datetime, ) + self.household_member.natural_key()
    natural_key.dependencies = ['member.householdmember', ]

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = "Clinic Enrollment Loss"
        verbose_name_plural = "Clinic Enrollment Loss"
        proxy = True
