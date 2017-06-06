from django.db import models


class ClinicModelManager(models.Manager):
    """Manager for all scheduled models (those with a clinic_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        ClinicVisit = models.get_model('bcpp_clinic', 'ClinicVisit')
        clinic_visit = ClinicVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(clinic_visit=clinic_visit)
