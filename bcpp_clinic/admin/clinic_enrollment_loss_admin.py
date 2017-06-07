from django.contrib import admin

from .model_admin_mixin import ModelAdminMixin
from ..admin_site import bcpp_clinic_admin
from ..forms import ClinicEnrollmentLossForm
from ..models import ClinicEnrollmentLoss


@admin.register(ClinicEnrollmentLoss, site=bcpp_clinic_admin)
class ClinicEnrollmentLossAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ClinicEnrollmentLossForm

    fields = ('clinic_eligibility', 'report_datetime', 'reason')

    list_display = (
        'report_datetime', 'reason', 'user_created',
        'user_modified', 'hostname_created')

    list_filter = ('report_datetime', 'reason', 'user_created',
                   'user_modified', 'hostname_created')

    radio_fields = {}

    instructions = []
