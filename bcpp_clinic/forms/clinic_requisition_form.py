from django import forms

from edc_lab.forms import RequisitionFormMixin
from bcpp_clinic.models.clinic_requisition import ClinicRequisition
from bcpp_subject.forms.form_mixins import SubjectModelFormMixin

from edc_base.modelform_mixins import (
    CommonCleanModelFormMixin, OtherSpecifyValidationMixin,
    ApplicableValidationMixin, Many2ManyModelValidationMixin,
    RequiredFieldValidationMixin, JSONModelFormMixin)
from bcpp_clinic.models.clinic_visit import ClinicVisit


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
