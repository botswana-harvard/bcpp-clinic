from simple_history.models import HistoricalRecords as AuditTrail
from edc_offstudy.models import OffStudyModelMixin


class ClinicOffStudy(OffStudyModelMixin):
    """A model completed by the user to indicate a subject is no longer on study."""
    history = AuditTrail()

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Off Study"
        verbose_name_plural = "Clinic Off Study"
