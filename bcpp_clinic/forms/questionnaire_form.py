from django import forms

from edc_constants.constants import YES

from ..models import Questionnaire
from .modelform_mixin import ClinicModelFormMixin


class QuestionnaireForm (ClinicModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('knows_last_cd4') == YES and not cleaned_data.get('cd4_count'):
            raise forms.ValidationError(
                'Participant answered that they know their last '
                'CD4 value, please provide this value.')

        if cleaned_data.get('knows_last_cd4') != YES and cleaned_data.get('cd4_count'):
            raise forms.ValidationError(
                f'Participant answered \'{cleaned_data.get("knows_last_cd4")}\' '
                'to knowledge of their CD4 result. Do not provide this value.')

        return cleaned_data

    class Meta:
        model = Questionnaire
        fields = '__all__'
