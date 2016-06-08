from django.contrib import admin

from ..filters import ClinicCommunityListFilter
from ..forms import ClinicSubjectLocatorForm
from ..models import ClinicSubjectLocator

from .clinic_visit_model_admin import ClinicVisitModelAdmin


class ClinicSubjectLocatorAdmin(ClinicVisitModelAdmin):

    form = ClinicSubjectLocatorForm
    fields = (
        'clinic_visit',
        'date_signed',
        'mail_address',
        'home_visit_permission',
        'physical_address',
        'may_follow_up',
        'may_sms_follow_up',
        'subject_cell',
        'subject_cell_alt',
        'subject_phone',
        'subject_phone_alt',
        'may_contact_someone',
        'contact_name',
        'contact_rel',
        'contact_physical_address',
        'contact_cell',
        'alt_contact_cell_number',
        'contact_phone',
        'has_alt_contact',
        'alt_contact_name',
        'alt_contact_rel',
        'alt_contact_cell',
        'other_alt_contact_cell',
        'alt_contact_tel',
        'may_call_work',
        'subject_work_place',
        'subject_work_phone',)
    radio_fields = {
        "home_visit_permission": admin.VERTICAL,
        "may_follow_up": admin.VERTICAL,
        "may_sms_follow_up": admin.VERTICAL,
        "has_alt_contact": admin.VERTICAL,
        "may_call_work": admin.VERTICAL,
        "may_contact_someone": admin.VERTICAL, }

    list_filter = (
        'may_follow_up', 'may_contact_someone', 'may_call_work', "home_visit_permission", ClinicCommunityListFilter)

    list_display = ('clinic_visit', 'date_signed', "home_visit_permission", "may_follow_up",
                    "may_sms_follow_up", "has_alt_contact", "may_call_work", "may_contact_someone")

admin.site.register(ClinicSubjectLocator, ClinicSubjectLocatorAdmin)
