from django import forms

from edc_base.modelform_mixins.json_modelform_mixin import JSONModelFormMixin
from edc_base.modelform_mixins.required_field_validation_mixin import RequiredFieldValidationMixin
from edc_base.modelform_mixins.many_to_many_validation_mixin import Many2ManyModelValidationMixin
from edc_base.modelform_mixins.applicable_validation_mixin import ApplicableValidationMixin
from edc_base.modelform_mixins.other_specify_validation_mixin import OtherSpecifyValidationMixin
from edc_base.modelform_mixins.common_clean_modelform_mixin import CommonCleanModelFormMixin

from ..models.clinic_visit import ClinicVisit


class CLinicModelFormMixin(CommonCleanModelFormMixin,
                           OtherSpecifyValidationMixin,
                           ApplicableValidationMixin,
                           Many2ManyModelValidationMixin,
                           RequiredFieldValidationMixin,
                           JSONModelFormMixin,
                           forms.ModelForm):

    visit_model = ClinicVisit
