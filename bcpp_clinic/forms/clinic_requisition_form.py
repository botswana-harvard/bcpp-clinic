from edc_lab.forms import RequisitionFormMixin

from ..models import ClinicRequisition
from .modelform_mixin import ClinicModelFormMixin


class ClinicRequisitionForm(RequisitionFormMixin, ClinicModelFormMixin):

    class Meta:
        model = ClinicRequisition
        fields = '__all__'
