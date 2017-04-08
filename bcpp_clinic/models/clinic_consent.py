from bcpp_subject.models import SubjectConsent
from edc_consent.model_mixins import ConsentModelMixin


class ClinicConsent(SubjectConsent):
    """ A model completed by the user that captures the ICF.
    """
    def __str__(self):
        return '{0} ({1}) V{2}'.format(
            self.subject_identifier,
            self.survey_schedule_object.name,
            self.version)

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Consent RBD'
        verbose_name_plural = 'Clinic Consent RBD'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )
