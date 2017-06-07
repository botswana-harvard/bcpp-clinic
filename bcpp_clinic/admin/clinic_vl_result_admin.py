from django.contrib import admin

from ..forms import ClinicVlResultForm
from ..models import ClinicVlResult
from ..admin_site import bcpp_clinic_admin
from ..admin import CrfModelAdminMixin


@admin.register(ClinicVlResult, site=bcpp_clinic_admin)
class ClinicVlResultAdmin(CrfModelAdminMixin, admin.ModelAdmin):

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

    list_display = ('clinic_visit', 'clinician_initials',
                    'collection_datetime', 'result_value', 'validated_by')

    search_fields = (
        'clinic_visit__subject_identifier',
        'clinician_initials', 'result_value',)
