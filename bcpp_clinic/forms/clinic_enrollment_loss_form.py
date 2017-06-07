from ..models import ClinicEnrollmentLoss
from .model_form_mixin import CLinicModelFormMixin


class ClinicEnrollmentLossForm(CLinicModelFormMixin):

    def clean(self):
        cleaned_data = super(ClinicEnrollmentLossForm, self).clean()

        return cleaned_data

    class Meta:
        model = ClinicEnrollmentLoss
        fields = '__all__'
