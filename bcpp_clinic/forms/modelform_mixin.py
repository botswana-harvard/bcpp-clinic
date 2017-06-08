from django import forms

from edc_base.modelform_mixins import JSONModelFormMixin, CommonCleanModelFormMixin

from ..models.clinic_visit import ClinicVisit


class ClinicModelFormMixin(CommonCleanModelFormMixin, JSONModelFormMixin, forms.ModelForm):

    visit_model = ClinicVisit
