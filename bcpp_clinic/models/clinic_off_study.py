from edc_base.audit_trail import AuditTrail
from edc.subject.off_study.models import BaseOffStudy


class ClinicOffStudy(BaseOffStudy):
    """A model completed by the user to indicate a subject is no longer on study."""
    history = AuditTrail()

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Off Study"
        verbose_name_plural = "Clinic Off Study"
