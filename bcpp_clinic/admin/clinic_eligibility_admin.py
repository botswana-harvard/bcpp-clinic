from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import ClinicEligibilityForm
from ..models import ClinicEligibility, ClinicHouseholdMember


class ClinicEligibilityAdmin(BaseModelAdmin):

    form = ClinicEligibilityForm

    instructions = ['This form is a tool to assist the Interviewer to confirm the '
                    'Eligibility status of the subject. After entering the required items, click SAVE.']

    fields = (
        'report_datetime',
        'first_name',
        'initials',
        'dob',
        'verbal_age',
        'gender',
        'has_identity',
        'identity',
        'identity_type',
        "citizen",
        "legal_marriage",
        "marriage_certificate",
        "part_time_resident",
        "literacy",
        "guardian",
        'inability_to_participate',
        "hiv_status",
    )

    list_display = ('household_member', 'report_datetime', 'gender', 'is_eligible', 'is_consented', 'is_refused')

    list_filter = ('gender', 'is_eligible', 'is_consented', 'is_refused', 'report_datetime', 'community')

    radio_fields = {
        'has_identity': admin.VERTICAL,
        "gender": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "legal_marriage": admin.VERTICAL,
        "marriage_certificate": admin.VERTICAL,
        "part_time_resident": admin.VERTICAL,
        "literacy": admin.VERTICAL,
        "guardian": admin.VERTICAL,
        "inability_to_participate": admin.VERTICAL,
        "hiv_status": admin.VERTICAL,
    }

    search_fields = (
        'household_member',
        'first_name',
        'initials',
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = ClinicHouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(ClinicEligibilityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ClinicEligibility, ClinicEligibilityAdmin)
