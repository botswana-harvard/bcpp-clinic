from django import forms

from ..models import ClinicEnrollmentLoss


class ClinicEnrollmentLossForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ClinicEnrollmentLossForm, self).clean()

        return cleaned_data

    class Meta:
        model = ClinicEnrollmentLoss
        fields = '__all__'
