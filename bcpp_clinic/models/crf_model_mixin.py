from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model_managers.historical_records import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel, FormAsJSONModelMixin
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow

from edc_metadata.model_mixins.updates import UpdatesCrfMetadataModelMixin

from edc_offstudy.model_mixins import OffstudyMixin

from edc_protocol.validators import datetime_not_before_study_start

from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import (
    CrfModelMixin as VisitTrackingCrfModelMixin, PreviousVisitModelMixin)

from edc_consent.model_mixins import RequiresConsentMixin as BaseRequiresConsentMixin

from .clinic_visit import ClinicVisit


class CrfModelManager(VisitTrackingCrfModelManager):

    def get_by_natural_key(self, subject_identifier, visit_schedule_name,
                           schedule_name, visit_code):
        return self.get(
            clinic_visit__subject_identifier=subject_identifier,
            clinic_visit__visit_schedule_name=visit_schedule_name,
            clinic_visit__schedule_name=schedule_name,
            clinic_visit__visit_code=visit_code
        )


class CrfModelMixin(VisitTrackingCrfModelMixin, OffstudyMixin,
                    BaseRequiresConsentMixin, PreviousVisitModelMixin,
                    UpdatesCrfMetadataModelMixin,
                    FormAsJSONModelMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`CLiinicVisit`).
    """

    clinic_visit = models.OneToOneField(ClinicVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_future, datetime_not_before_study_start],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    history = HistoricalRecords()

    def natural_key(self):
        return self.clinic_visit.natural_key()
    natural_key.dependencies = ['bcpp_clinic.clinicvisit']

    class Meta(VisitTrackingCrfModelMixin.Meta, BaseRequiresConsentMixin.Meta):
        consent_model = 'bcpp_clinic.clinicconsent'
        abstract = True
