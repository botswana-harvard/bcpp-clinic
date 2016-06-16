from django.contrib import admin

from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from ..models import ClinicEligibility


from ..models import ClinicRefusalHistory


class ClinicRefusalHistoryAdmin(BaseRegisteredSubjectModelAdmin):

    fields = (
        'clinic_eligibility',
        'report_datetime',
        'refusal_date',
        'reason',
        'reason_other')

    radio_fields = {"reason": admin.VERTICAL}

    list_display = ('clinic_eligibility', 'report_datetime', )

    search_fields = [
        'clinic_eligibility__first_name']

    list_filter = ('reason')

    instructions = []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "clinic_eligibility":
            kwargs["queryset"] = ClinicEligibility.objects.filter(id__exact=request.GET.get('clinic_eligibility', 0))
        return super(ClinicRefusalHistoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ClinicRefusalHistory, ClinicRefusalHistoryAdmin)
