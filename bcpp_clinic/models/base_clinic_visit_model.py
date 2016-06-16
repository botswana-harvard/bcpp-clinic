from datetime import datetime

from django.db import models

from simple_history.models import HistoricalRecords as AuditTrail
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin
from edc_consent.models import RequiresConsentMixin

from .clinic_off_study_mixin import ClinicOffStudyMixin
from .clinic_visit import ClinicVisit

from ..managers import ClinicModelManager


class BaseClinicVisitModel(SyncModelMixin, ClinicOffStudyMixin, RequiresConsentMixin, BaseUuidModel):

    """ Base model for all clinic scheduled models (adds key to :class:`ClinicVisit`). """

    clinic_visit = models.OneToOneField(ClinicVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Report date/time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),
    )

    objects = ClinicModelManager()

    history = AuditTrail()

    def natural_key(self):
        return self.get_visit().natural_key()

    def __unicode__(self):
        return unicode(self.get_visit())

    def get_report_datetime(self):
        return self.get_visit().report_datetime

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_visit(self):
        return self.clinic_visit

    class Meta:
        abstract = True
