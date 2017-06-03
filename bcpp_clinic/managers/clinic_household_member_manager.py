from django.db import models


class ClinicHouseholdMemberManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)
