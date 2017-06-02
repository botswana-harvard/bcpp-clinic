from django.contrib import admin

from ..forms import ViralLoadTrackingForm
from bcpp_clinic.admin_site import bcpp_clinic_admin
from bcpp_clinic.admin.model_admin_mixin import CrfModelAdminMixin
from bcpp_clinic.models.viral_load_tracking import ViralLoadTracking


@admin.register(ViralLoadTracking, site=bcpp_clinic_admin)
class ViralLoadTrackingAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ViralLoadTrackingForm
    fields = ('clinic_visit',
              'report_datetime',
              'is_drawn',
              'reason_not_drawn',
              'drawn_datetime',
              'clinician_initials',)
    list_display = ('clinic_visit', 'is_drawn', 'reason_not_drawn', 'drawn_datetime')
    list_filter = ('is_drawn',)
    radio_fields = {}
