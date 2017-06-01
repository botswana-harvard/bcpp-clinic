from member.models import EnrollmentLoss


class ClinicEnrollmentLoss(EnrollmentLoss):

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = "Clinic Enrollment Loss"
        verbose_name_plural = "Clinic Enrollment Loss"
        proxy = True
