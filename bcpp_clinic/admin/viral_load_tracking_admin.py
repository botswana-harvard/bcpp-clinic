from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import ViralLoadTrackingForm
from ..models import ViralLoadTracking, ClinicVisit


class ViralLoadTrackingAdmin(BaseModelAdmin):

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
admin.site.register(ViralLoadTracking, ViralLoadTrackingAdmin)
