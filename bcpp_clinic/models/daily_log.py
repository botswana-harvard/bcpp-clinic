from datetime import date

from django.db import models

from edc.device.sync.models import BaseSyncUuidModel

from ..managers import DailyLogManager


class DailyLog(BaseSyncUuidModel):
    """A model completed by the user daily to help measure the daily flow
    of patients in the clinic."""

    report_date = models.DateField(
        default=date.today(),
        # unique=True
    )

    from_pharma = models.IntegerField(
        verbose_name='Number of patients referred from pharmacy',
    )

    from_nurse_prescriber = models.IntegerField(
        verbose_name='Number of patients referred from nurse prescriber',
    )

    from_ssc = models.IntegerField(
        verbose_name='Number of patients referred from SSC',
    )

    from_other = models.IntegerField(
        verbose_name='Number of patients referred from \'other\'',
    )

    idcc_scheduled = models.IntegerField(
        verbose_name='Number of patients scheduled/booked for appointments in the IDCC',
    )

    idcc_newly_registered = models.IntegerField(
        verbose_name='Number of patients newly registered to the IDCC',
    )

    idcc_no_shows = models.IntegerField(
        verbose_name='Number of patients who did not show up for their appointment.',
    )

    approached = models.IntegerField(
        verbose_name='Number of patients approached',
    )

    refused = models.IntegerField(
        verbose_name='Number of patients who refused to complete the eligibility checklist',
    )

    def __unicode__(self):
        return self.report_date.strftime('%Y-%m-%d')

    def natural_key(self):
        return (self.report_date, )

    objects = DailyLogManager()

    class Meta:
        app_label = 'bcpp_clinic'
        unique_together = ['report_date', 'hostname_created']
