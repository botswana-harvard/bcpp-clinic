from member.models import HouseholdMember


class ClinicHouseholdMember(HouseholdMember):
    """A proxy model of member.HouseholdMember concrete model.
    """

    def __str__(self):
        return '{0} {1} {2}{3} {4}'.format(
            self.first_name,
            self.initials,
            self.age_in_years,
            self.gender,
            'clinic-member')

    class Meta:
        proxy = True
