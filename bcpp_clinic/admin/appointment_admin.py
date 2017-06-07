from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_visit_schedule.admin import (
    visit_schedule_fieldset_tuple, visit_schedule_fields)

from .model_admin_mixin import ModelAdminMixin

from ..models import Appointment

from ..admin_site import bcpp_clinic_admin
from ..forms import AppointmentForm


@admin.register(Appointment, site=bcpp_clinic_admin)
class AppointmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = AppointmentForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'appt_datetime',
                'appt_type',
                'appt_status',
                'appt_reason',
                'comment',
            ]}),
        visit_schedule_fieldset_tuple,
        audit_fieldset_tuple)

    list_display = (
        'subject_identifier', 'visit_code', 'appt_datetime', 'appt_status')

    list_filter = ('visit_code', 'appt_datetime', 'appt_status', 'appt_type')

    search_fields = ('subject_identifier', )

    radio_fields = {
        'appt_type': admin.VERTICAL,
        'appt_status': admin.VERTICAL}

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj)
                + visit_schedule_fields
                + ('subject_identifier',))
