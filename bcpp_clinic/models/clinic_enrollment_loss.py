from datetime import datetime

from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel
from edc_map.classes import site_mappers

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..managers import BaseClinicHouseholdMemberManager


class ClinicEnrollmentLoss(BaseSyncUuidModel):
    """A model completed by the system triggered by an ineligible potential participant.

    This model is deleted if the criteria is changed resulting in an eligible potential
    participant."""

    household_member = models.OneToOneField(HouseholdMember, null=True)

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

    objects = BaseClinicHouseholdMemberManager()

    def save(self, *args, **kwargs):
        self.community = site_mappers.get_mapper(site_mappers.current_community).map_area
        super(ClinicEnrollmentLoss, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.household_member)

    def natural_key(self):
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.householdmember', ]

    def loss_reason(self):
        return '; '.join(self.reason or [])
    loss_reason.allow_tags = True

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Enrollment Loss'
        verbose_name_plural = 'Clinic Enrollment Loss'
