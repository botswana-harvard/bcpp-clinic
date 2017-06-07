from edc_consent.modelform_mixins import ConsentModelFormMixin

from ..models import ClinicConsent
from .model_form_mixin import CLinicModelFormMixin


class ClinicConsentForm(ConsentModelFormMixin, CLinicModelFormMixin):

    class Meta:
        model = ClinicConsent
        fields = '__all__'
