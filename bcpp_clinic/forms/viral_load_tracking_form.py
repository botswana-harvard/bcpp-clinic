from django import forms

from edc_constants.constants import YES

from ..models import ViralLoadTracking
from .modelform_mixin import ClinicModelFormMixin


class ViralLoadTrackingForm(ClinicModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_drawn') == YES and not cleaned_data.get('clinician_initials'):
            raise forms.ValidationError(
                'If sample was drawn, please provide the Clinician\'s initials')

        if cleaned_data.get('is_drawn') == YES and not cleaned_data.get('drawn_datetime'):
            raise forms.ValidationError(
                'If sample was drawn, please provide the date/time sample drawn initials')

        return cleaned_data

    class Meta:
        model = ViralLoadTracking
        fields = '__all__'
