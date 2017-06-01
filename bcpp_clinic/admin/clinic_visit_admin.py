from django.contrib import admin

from ..forms import ClinicVisitForm
from ..models import ClinicVisit, ClinicEligibility
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin
from bcpp_clinic.admin_site import bcpp_clinic_admin
from bcpp_clinic.admin.model_admin_mixin import ModelAdminMixin
from member.models.household_member.household_member import HouseholdMember
from bcpp_clinic.models.clinic_requisition import ClinicRequisition


@admin.register(ClinicVisit, site=bcpp_clinic_admin)
class ClinicVisitAdmin(VisitModelAdminMixin, ModelAdminMixin, admin.ModelAdmin):

    form = ClinicVisitForm

    requisition_model = ClinicRequisition

    dashboard_type = 'clinic'

    list_display = (
        'appointment',
        'report_datetime',
        'reason',
        "info_source",
        'created',
        'user_created',
    )

    list_filter = (
        'report_datetime',
        'reason',
        'household_member__household_structure__household__community',
        'appointment__appt_status',
        'appointment__visit_definition__code',
    )

    search_fields = (
        'appointment__registered_subject__subject_identifier',
        'appointment__registered_subject__registration_identifier',
        'appointment__registered_subject__first_name',
        'appointment__registered_subject__identity',
    )

    fields = (
        'household_member',
        "appointment",
        "report_datetime",
        "comments"
    )
