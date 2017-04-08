from member.models import EnrollmentChecklist


class ClinicEligibility(EnrollmentChecklist):
    """A model completed by the user that captures and confirms
    enrollment eligibility criteria.
    """

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Eligibility"
        verbose_name_plural = "Clinic Eligibility"
        unique_together = (('household_member', 'report_datetime'), )
        ordering = ['-report_datetime']
