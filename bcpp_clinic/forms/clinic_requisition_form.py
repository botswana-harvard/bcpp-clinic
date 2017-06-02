from django import forms

from edc_base.modelform_mixins import (
    CommonCleanModelFormMixin, OtherSpecifyValidationMixin,
    ApplicableValidationMixin, Many2ManyModelValidationMixin,
    RequiredFieldValidationMixin, JSONModelFormMixin)
from edc_lab.forms import RequisitionFormMixin

from ..models import ClinicRequisition, ClinicVisit


class SubjectModelFormMixin(CommonCleanModelFormMixin,
                            OtherSpecifyValidationMixin,
                            ApplicableValidationMixin,
                            Many2ManyModelValidationMixin,
                            RequiredFieldValidationMixin,
                            JSONModelFormMixin,
                            forms.ModelForm):

    visit_model = ClinicVisit

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class ClinicRequisitionForm(RequisitionFormMixin, SubjectModelFormMixin):

    class Meta:
        model = ClinicRequisition
        fields = '__all__'
