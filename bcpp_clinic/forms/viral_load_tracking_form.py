from django import forms

from ..models import ViralLoadTracking
from .base_clinic_model_form import BaseClinicModelForm


class ViralLoadTrackingForm(BaseClinicModelForm):

    def clean(self):

        cleaned_data = super(ViralLoadTrackingForm, self).clean()

        if cleaned_data.get('is_drawn', None) == 'Yes' and not cleaned_data.get('clinician_initials', None):
            raise forms.ValidationError('If sample was drawn, please provide the Clinician\'s initials')

        if cleaned_data.get('is_drawn', None) == 'Yes' and not cleaned_data.get('drawn_datetime', None):
            raise forms.ValidationError('If sample was drawn, please provide the date/ time sample drawn initials')

        return cleaned_data

    class Meta:
        model = ViralLoadTracking
