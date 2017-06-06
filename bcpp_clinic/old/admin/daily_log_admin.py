from django.contrib import admin

from ..admin import ModelAdminMixin
from ..admin_site import bcpp_clinic_admin
from ..forms import DailyLogForm
from ..models import DailyLog


@admin.register(DailyLog, site=bcpp_clinic_admin)
class DailyLogAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DailyLogForm

    fields = (
        'report_date',
        'from_pharma',
        'from_nurse_prescriber',
        'from_ssc',
        'from_other',
        'idcc_scheduled',
        'idcc_newly_registered',
        'idcc_no_shows',
        'approached',
        'refused')

    list_display = (
        'report_date',
        'from_pharma',
        'from_nurse_prescriber',
        'from_ssc',
        'from_other',
        'idcc_scheduled',
        'idcc_newly_registered',
        'idcc_no_shows',
        'approached',
        'refused')

    list_filter = ('report_date', )

    radio_fields = {}

    instructions = ['Complete this form once per day.']
