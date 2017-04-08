from bcpp_subject.models import SubjectLocator


class ClinicSubjectLocator(SubjectLocator):

    def __str__(self):
        return self.clinic_visit

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = "Clinic Subject Locator"
        verbose_name_plural = "Clinic Subject Locator"
        proxy = True
