from django.contrib import admin

from ..forms import ClinicEligibilityForm

from edc_registration.models import RegisteredSubject
from bcpp_clinic.models.clinic_eligibility import ClinicEligibility
from edc_base.fieldsets.fieldsets_modeladmin_mixin import FieldsetsModelAdminMixin
from bcpp_clinic.admin_site import bcpp_clinic_admin
from bcpp_clinic.admin.model_admin_mixin import ModelAdminMixin


@admin.register(ClinicEligibility, site=bcpp_clinic_admin)
class ClinicEligibilityAdmin(ModelAdminMixin, FieldsetsModelAdminMixin, admin.ModelAdmin):

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

    list_display = ('report_datetime', 'gender', 'is_eligible', 'is_consented', 'is_refused')

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
        'registered_subject',
        'first_name',
        'initials',
    )
