from django.contrib import admin

from bcpp_clinic.admin_site import bcpp_clinic_admin
from bcpp_clinic.forms.clinic_refused_member_form import ClinicRefusedMemberForm
from bcpp_clinic.models.clinic_refused_member import ClinicRefusedMember
from bcpp_clinic.models.clinic_eligibility import ClinicEligibility
from bcpp_clinic.admin.model_admin_mixin import ModelAdminMixin


@admin.register(ClinicRefusedMember, site=bcpp_clinic_admin)
class ClinicRefusedMemberAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ClinicRefusedMemberForm

    fields = ('clinic_eligibility',
              'refusal_date',
              'reason',
              'reason_other',
              'comment')

    list_display = ('clinic_eligibility',
                    'refusal_date',
                    'community',
                    'user_created',
                    'user_modified',
                    'hostname_created')

    list_filter = ('community',
                   'created',
                   'user_created',
                   'user_modified',
                   'hostname_created')

    radio_fields = {
        "reason": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "clinic_eligibility":
            kwargs["queryset"] = ClinicEligibility.objects.filter(id__exact=request.GET.get('clinic_eligibility', 0))
        return super(ClinicRefusedMemberAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
