from django import forms

from ..models import ClinicConsent
from edc_consent.modelform_mixins import ConsentModelFormMixin


class ClinicConsentForm(ConsentModelFormMixin, forms.ModelForm):

    class Meta:
        model = ClinicConsent
        fields = '__all__'
