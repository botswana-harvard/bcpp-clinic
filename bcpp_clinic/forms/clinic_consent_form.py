from edc_consent.modelform_mixins import ConsentModelFormMixin

from ..models import ClinicConsent
from .modelform_mixin import ClinicModelFormMixin


class ClinicConsentForm(ConsentModelFormMixin, ClinicModelFormMixin):

    class Meta:
        model = ClinicConsent
        fields = '__all__'
