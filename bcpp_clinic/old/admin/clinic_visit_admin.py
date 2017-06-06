from django.contrib import admin


from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from .model_admin_mixin import ModelAdminMixin
from ..admin_site import bcpp_clinic_admin
from ..forms import ClinicVisitForm
from ..models import ClinicRequisition
from ..models import ClinicVisit


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
        'clinic_household_member__household_structure__household__plot__map_area',
        'appointment__appt_status',
        'appointment__visit_code',
    )

    search_fields = (
        'appointment__subject_identifier',
    )
