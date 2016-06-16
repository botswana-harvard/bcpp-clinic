from datetime import datetime

from django.db import models

from simple_history.models import HistoricalRecords as AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin

from .clinic_eligibility import ClinicEligibility

# from ..managers import BaseClinicHouseholdMemberManager


class ClinicEnrollmentLoss(SyncModelMixin, BaseUuidModel):
    """A model completed by the system triggered by an ineligible potential participant.

    This model is deleted if the criteria is changed resulting in an eligible potential
    participant."""

    clinic_eligibility = models.OneToOneField(ClinicEligibility, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=datetime.today(),
        help_text='Date and time of report.'
    )

    reason = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='A list of reasons delimited by \';\'. From clinic_eligibility.loss_reason.'
    )

    community = models.CharField(max_length=25, editable=False)

    history = AuditTrail()

#     objects = BaseClinicHouseholdMemberManager()

    def save(self, *args, **kwargs):
        super(ClinicEnrollmentLoss, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.clinic_eligibility)

    def natural_key(self):
        return self.clinic_eligibility.natural_key()
    natural_key.dependencies = ['bcpp_clinic.clinic_eligibility', ]

    def loss_reason(self):
        return '; '.join(self.reason or [])
    loss_reason.allow_tags = True

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Enrollment Loss'
        verbose_name_plural = 'Clinic Enrollment Loss'
