from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import ClinicRefusalForm
from ..models import ClinicRefusal, ClinicEligibility


class ClinicRefusalAdmin(BaseModelAdmin):

    form = ClinicRefusalForm

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
        return super(ClinicRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ClinicRefusal, ClinicRefusalAdmin)
