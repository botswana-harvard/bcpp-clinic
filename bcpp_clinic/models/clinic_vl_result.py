from bcpp_subject.models import ViralLoadResult
from bcpp_subject.models.model_mixins.crf_model_mixin import CrfModelMixin


class ClinicVlResult(ViralLoadResult):
    pass

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_clinic"
        verbose_name = "Clinic VL Result"
        verbose_name_plural = "Clinic VL Result"
        proxy = True
