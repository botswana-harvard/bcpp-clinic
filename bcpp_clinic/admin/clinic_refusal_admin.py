from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import ClinicRefusalForm
from ..models import ClinicRefusal, ClinicHouseholdMember


class ClinicRefusalAdmin(BaseModelAdmin):

    form = ClinicRefusalForm

    fields = ('household_member',
              'refusal_date',
              'reason',
              'reason_other',
              'comment')

    list_display = ('household_member',
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
        if db_field.name == "household_member":
            kwargs["queryset"] = ClinicHouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(ClinicRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ClinicRefusal, ClinicRefusalAdmin)
