from .clinic_off_study import ClinicOffStudy

from edc_offstudy.models import OffStudyMixin


class ClinicOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL = ClinicOffStudy

    class Meta:
        abstract = True
