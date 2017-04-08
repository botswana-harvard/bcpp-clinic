from django import forms

from ..models import ClinicConsent
from bcpp_subject.forms.subject_consent_form import ConsentModelFormMixin


class ClinicConsentForm(ConsentModelFormMixin, forms.ModelForm):

    class Meta:
        model = ClinicConsent
