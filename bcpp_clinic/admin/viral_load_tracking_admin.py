from django.contrib import admin

from ..forms import ViralLoadTrackingForm
from ..models import ViralLoadTracking, ClinicVisit
from bcpp_clinic.admin_site import bcpp_clinic_admin
from bcpp_clinic.admin.model_admin_mixin import CrfModelAdminMixin


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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "clinic_visit":
            try:
                ClinicVisit.objects.get(id=request.GET.get('clinic_visit'))
                clinic_visits = ClinicVisit.objects.filter(id=request.GET.get('clinic_visit'))
            except ClinicVisit.DoesNotExist:
                clinic_visits = ClinicVisit.objects.none()
            kwargs["queryset"] = clinic_visits
        return super(ViralLoadTrackingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
