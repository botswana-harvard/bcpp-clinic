from django.contrib import admin

from ..admin import CrfModelAdminMixin
from ..admin_site import bcpp_clinic_admin
from ..forms import ViralLoadTrackingForm
from ..models import ViralLoadTracking


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
