from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from edc_base.modeladmin_mixins.model_admin_redirect_on_delete_mixin import ModelAdminRedirectOnDeleteMixin
from edc_base.fieldsets.fieldsets_modeladmin_mixin import FieldsetsModelAdminMixin
from edc_base.modeladmin_mixins.form_as_json_model_admin_mixin import FormAsJSONModelAdminMixin
from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)

from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class CrfModelAdminMixin(VisitTrackingCrfModelAdminMixin,
                         ModelAdminRedirectOnDeleteMixin,
                         ModelAdminMixin,
                         FieldsetsModelAdminMixin,
                         FormAsJSONModelAdminMixin,
                         admin.ModelAdmin):

    post_url_on_delete_name = 'bcpp_clinic:dashboard_url'
    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. '
        'Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(
            subject_identifier=obj.subject_identifier,
            household_identifier=(
                obj.clinic_visit
                .household_member
                .household_structure
                .household
                .household_identifier),
            appointment=str(obj.clinic_visit.appointment.id),
            survey_schedule=obj.subject_visit.survey_schedule_object.field_value,
            survey=obj.subject_visit.survey_object.field_value)

    def view_on_site(self, obj):
        household_member = obj.clinic_visit.household_member
        try:
            return reverse(
                'bcpp_clinic:dashboard_url', kwargs=dict(
                    subject_identifier=household_member.subject_identifier,
                    household_identifier=(household_member.household_structure.
                                          household.household_identifier),
                    survey=obj.clinic_visit.survey_object.field_value,
                    survey_schedule=obj.clinic_visit.survey_schedule_object.field_value))
        except NoReverseMatch:
            return super().view_on_site(obj)
