from django.contrib import admin

from ..admin import CrfModelAdminMixin
from ..admin_site import bcpp_clinic_admin
from ..filters import ClinicCommunityListFilter
from ..forms import QuestionnaireForm
from ..models import Questionnaire


@admin.register(Questionnaire, site=bcpp_clinic_admin)
class QuestionnaireAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = QuestionnaireForm
    fields = (
        "clinic_visit",
        "report_datetime",
        "registration_type",
        "on_arv",
        "knows_last_cd4",
        "cd4_count",
    )
    radio_fields = {
        "registration_type": admin.VERTICAL,
        "on_arv": admin.VERTICAL,
        "knows_last_cd4": admin.VERTICAL,
    }
    list_display = ('clinic_visit', 'registration_type', 'on_arv', 'cd4_count', 'report_datetime')
    list_filter = ('on_arv', ClinicCommunityListFilter, 'report_datetime')
    search_fields = ('on_arv',)
    instructions = [("Note to Interviewer: The OTHER NON Viral LOAD visit also refers to:"
                     " A patient who may be coming in for a: i. Drug Refill, ii. CD4 count"
                     " iii. Phlebotomy, iv. Sick visit, etc ")]
