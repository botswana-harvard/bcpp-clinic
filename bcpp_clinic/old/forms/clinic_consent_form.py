from django import forms

from edc_consent.modelform_mixins import ConsentModelFormMixin

from ..models import ClinicConsent


class ClinicConsentForm(ConsentModelFormMixin, forms.ModelForm):

    class Meta:
        model = ClinicConsent
        fields = '__all__'
