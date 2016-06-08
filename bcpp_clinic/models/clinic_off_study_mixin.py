from .clinic_off_study import ClinicOffStudy

from edc.subject.off_study.mixins import OffStudyMixin


class ClinicOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL = ClinicOffStudy

    class Meta:
        abstract = True
