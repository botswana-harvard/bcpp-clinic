from django.contrib import admin

from ..admin_site import bcpp_clinic_admin
from .model_admin_mixin import ModelAdminMixin
from ..models import ClinicRefusedMember
from ..forms import ClinicRefusedMemberForm


@admin.register(ClinicRefusedMember, site=bcpp_clinic_admin)
class ClinicRefusedMemberAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ClinicRefusedMemberForm

    fields = ('refusal_date',
              'reason',
              'reason_other',
              'comment')

    list_display = ('refusal_date',
                    'user_created',
                    'user_modified',
                    'hostname_created')

    list_filter = ('created',
                   'user_created',
                   'user_modified',
                   'hostname_created')

    radio_fields = {
        "reason": admin.VERTICAL,
    }
