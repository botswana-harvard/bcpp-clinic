from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import ClinicEnrollmentLossForm
from ..models import ClinicEnrollmentLoss


class ClinicEnrollmentLossAdmin(BaseModelAdmin):

    form = ClinicEnrollmentLossForm

    fields = ('household_member', 'report_datetime', 'reason')

    list_display = (
        'household_member', 'report_datetime', 'reason', 'user_created', 'user_modified', 'hostname_created')

    list_filter = ('community', 'report_datetime', 'reason', 'user_created', 'user_modified', 'hostname_created')

    instructions = []
admin.site.register(ClinicEnrollmentLoss, ClinicEnrollmentLossAdmin)
