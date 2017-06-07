from django import forms

from ..models import Questionnaire
from .model_form_mixin import CLinicModelFormMixin


class QuestionnaireForm (CLinicModelFormMixin):

    def clean(self):

        cleaned_data = super(QuestionnaireForm, self).clean()

        if cleaned_data.get('knows_last_cd4', None) == 'Yes' and not cleaned_data.get('cd4_count', None):
            raise forms.ValidationError('Participant answered that they know their last '
                                        'CD4 value, please provide this value.')

        if cleaned_data.get('knows_last_cd4', None) != 'Yes' and cleaned_data.get('cd4_count', None):
            raise forms.ValidationError('Participant answered \'{0}\' to knowledge of '
                                        'their CD4 result. Do not provide this value.'.format(
                                            cleaned_data.get('knows_last_cd4', None)))

        return cleaned_data

    class Meta:
        model = Questionnaire
        fields = '__all__'
