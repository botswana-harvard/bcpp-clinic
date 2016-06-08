from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..filters import ClinicCommunityListFilter
from ..forms import ClinicVlResultForm
from ..models import ClinicVlResult, ClinicVisit


class ClinicVlResultAdmin(BaseModelAdmin):

    form = ClinicVlResultForm
    fields = (
        'clinic_visit',
        'report_datetime',
        'site',
        'clinician_initials',
        'collection_datetime',
        'assay_date',
        'result_value',
        'comment',
        'validation_date',
        'validated_by')

    list_display = ('clinic_visit', 'clinician_initials', 'collection_datetime', 'result_value', 'validated_by')
    list_filter = ('collection_datetime', ClinicCommunityListFilter, )

    search_fields = (
        'clinic_visit__appointment__registered_subject__subject_identifier', 'clinician_initials', 'result_value', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "clinic_visit":
            try:
                ClinicVisit.objects.get(id=request.GET.get('clinic_visit'))
                clinic_visits = ClinicVisit.objects.filter(id=request.GET.get('clinic_visit'))
            except ClinicVisit.DoesNotExist:
                clinic_visits = ClinicVisit.objects.none()
            kwargs["queryset"] = clinic_visits
        return super(ClinicVlResultAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ClinicVlResult, ClinicVlResultAdmin)
