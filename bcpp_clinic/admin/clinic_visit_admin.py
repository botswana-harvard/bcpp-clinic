from django.contrib import admin

from ..forms import ClinicVisitForm
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin
from bcpp_clinic.admin_site import bcpp_clinic_admin
from bcpp_clinic.admin.model_admin_mixin import ModelAdminMixin
from bcpp_clinic.models.clinic_requisition import ClinicRequisition
from bcpp_clinic.models.clinic_visit import ClinicVisit


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

    fieldsets = ()

    list_filter = (
        'report_datetime',
        'reason',
        'household_member__household_structure__household__plot__map_area',
        'appointment__appt_status',
        'appointment__visit_code',
    )

    search_fields = (
        'appointment__subject_identifier',
    )
