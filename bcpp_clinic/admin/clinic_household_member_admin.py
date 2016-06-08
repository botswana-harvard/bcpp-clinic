from django.contrib import admin

from bhp066.apps.bcpp_household_member.admin.base_household_member_admin import BaseHouseholdMemberAdmin

from ..models import ClinicHouseholdMember


class ClinicHouseholdMemberAdmin(BaseHouseholdMemberAdmin):
    pass

admin.site.register(ClinicHouseholdMember, ClinicHouseholdMemberAdmin)
