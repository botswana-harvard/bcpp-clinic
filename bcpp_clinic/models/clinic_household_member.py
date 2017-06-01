from member.models import HouseholdMember


class ClinicHouseholdMember(HouseholdMember):
    """A proxy model of member.HouseholdMember concrete model.
    """

    def __str__(self):
        return '{} {} {}{} {} {}'.format(
            self.first_name, self.initials, self.age_in_years,
            self.gender, self.household_structure.survey_schedule,
            'clinic-member')

    class Meta(HouseholdMember.Meta):
        app_label = 'bcpp_clinic'
        verbose_name = "Clinic Household Member"
        verbose_name_plural = "Clinic Household Member"
        proxy = True
