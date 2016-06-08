from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import ClinicEnrollmentLoss


class ClinicEnrollmentLossForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(ClinicEnrollmentLossForm, self).clean()

        return cleaned_data

    class Meta:
        model = ClinicEnrollmentLoss
