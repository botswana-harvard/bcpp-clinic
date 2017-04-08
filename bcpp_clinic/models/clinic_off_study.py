from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_offstudy.model_mixins import OffstudyModelMixin, OffstudyModelManager


class ClinicOffStudy(OffstudyModelMixin, BaseUuidModel):

    objects = OffstudyModelManager()

    history = HistoricalRecords()

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Off Study"
        verbose_name_plural = "Clinic Off Study"
