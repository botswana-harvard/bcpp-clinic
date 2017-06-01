from django.contrib import admin

from ..forms import ClinicEnrollmentLossForm
from ..models import ClinicEnrollmentLoss
from bcpp_clinic.admin_site import bcpp_clinic_admin
from bcpp_clinic.admin.model_admin_mixin import ModelAdminMixin


@admin.register(ClinicEnrollmentLoss, site=bcpp_clinic_admin)
class ClinicEnrollmentLossAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ClinicEnrollmentLossForm

    fields = ('clinic_eligibility', 'report_datetime', 'reason')

    list_display = (
        'clinic_eligibility', 'report_datetime', 'reason', 'user_created', 'user_modified', 'hostname_created')

    list_filter = ('community', 'report_datetime', 'reason', 'user_created', 'user_modified', 'hostname_created')

    instructions = []
