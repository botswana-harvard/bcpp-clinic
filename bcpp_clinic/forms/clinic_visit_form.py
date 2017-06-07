from edc_visit_tracking.form_mixins import VisitFormMixin

from ..models import ClinicVisit
from .model_form_mixin import CLinicModelFormMixin


class ClinicVisitForm (VisitFormMixin, CLinicModelFormMixin):

    class Meta:
        model = ClinicVisit
        fields = '__all__'
