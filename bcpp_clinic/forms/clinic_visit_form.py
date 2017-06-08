from edc_visit_tracking.form_mixins import VisitFormMixin

from ..models import ClinicVisit
from .modelform_mixin import ClinicModelFormMixin


class ClinicVisitForm (VisitFormMixin, ClinicModelFormMixin):

    class Meta:
        model = ClinicVisit
        fields = '__all__'
