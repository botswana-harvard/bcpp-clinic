from django.contrib import admin

from edc.subject.appointment.admin import BaseAppointmentModelAdmin

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_lab.models import ClinicRequisition

from ..forms import ClinicVisitForm
from ..models import ClinicVisit, ClinicEligibility


class ClinicVisitAdmin(BaseAppointmentModelAdmin):

    form = ClinicVisitForm

    visit_model_instance_field = 'clinic_visit'

    requisition_model = ClinicRequisition

    dashboard_type = 'clinic'

    list_display = (
        'appointment',
        'report_datetime',
        'reason',
        "info_source",
        'created',
        'user_created',
    )

    list_filter = (
        'report_datetime',
        'reason',
        'household_member__household_structure__household__community',
        'appointment__appt_status',
        'appointment__visit_definition__code',
    )

    search_fields = (
        'appointment__registered_subject__subject_identifier',
        'appointment__registered_subject__registration_identifier',
        'appointment__registered_subject__first_name',
        'appointment__registered_subject__identity',
    )

    fields = (
        'household_member',
        "appointment",
        "report_datetime",
        "comments"
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            try:
                HouseholdMember.objects.get(id=request.GET.get('household_member'))
                household_members = HouseholdMember.objects.filter(id=request.GET.get('household_member'))
            except HouseholdMember.DoesNotExist:
                try:
                    household_member = ClinicEligibility.objects.get(
                        id=request.GET.get('dashboard_id')).household_member
                    household_members = HouseholdMember.objects.filter(id=household_member.pk)
                except (HouseholdMember.DoesNotExist, ClinicEligibility.DoesNotExist):
                    household_members = HouseholdMember.objects.none()
            kwargs["queryset"] = household_members
        return super(ClinicVisitAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ClinicVisit, ClinicVisitAdmin)
