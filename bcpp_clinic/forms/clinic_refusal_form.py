from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import ClinicRefusal


class ClinicRefusalForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(ClinicRefusalForm, self).clean()

        return cleaned_data

    class Meta:
        model = ClinicRefusal
