from django.contrib import admin

from bcpp_clinic.admin_site import bcpp_clinic_admin
from bcpp_clinic.forms.clinic_refused_member_form import ClinicRefusedMemberForm
from bcpp_clinic.models.clinic_refused_member import ClinicRefusedMember
from bcpp_clinic.admin.model_admin_mixin import ModelAdminMixin


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
