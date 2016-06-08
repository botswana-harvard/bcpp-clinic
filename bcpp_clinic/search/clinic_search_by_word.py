from django.db.models import Q

from ..models import ClinicEligibility

from edc.dashboard.search.classes import BaseSearchByWord


class ClinicSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = ClinicEligibility
    order_by = ['-created']
    template = 'cliniceligibility_include.html'

    @property
    def qset(self):
        qset = (
            Q(household_member__registered_subject__subject_identifier__icontains=self.search_value) |
            Q(household_member__registered_subject__first_name__icontains=self.search_value)
        )
        return qset
