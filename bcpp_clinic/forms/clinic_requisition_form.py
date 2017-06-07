from edc_lab.forms import RequisitionFormMixin

from ..models import ClinicRequisition
from .model_form_mixin import CLinicModelFormMixin


class ClinicRequisitionForm(RequisitionFormMixin, CLinicModelFormMixin):

    class Meta:
        model = ClinicRequisition
        fields = '__all__'
