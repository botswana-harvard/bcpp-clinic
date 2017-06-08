from django import forms

from ..models import ClinicVlResult
from .modelform_mixin import ClinicModelFormMixin


class ClinicVlResultForm (ClinicModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        if (cleaned_data.get('assay_date', None)
                <= cleaned_data.get('collection_datetime', None).date()):
            raise forms.ValidationError(
                'Assay date CANNOT be less than or equal to '
                'the date sample drawn. Please correct.')
        return cleaned_data

    class Meta:
        model = ClinicVlResult
        fields = '__all__'
