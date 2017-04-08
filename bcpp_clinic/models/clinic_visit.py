from bcpp_subject.models import SubjectVisit
from edc_visit_tracking.model_mixins.visit_model_mixin import VisitModelMixin
from bcpp_subject.models.requires_consent_model_mixin import RequiresConsentMixin


class ClinicVisit(SubjectVisit):

    def save(self, *args, **kwargs):
        self.info_source = 'subject'
        self.reason = 'clinic RBD'
        self.appointment.appt_type = 'clinic'
        self.subject_identifier = self.appointment.subject_identifier
        super(ClinicVisit, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} {} ({}) {}'.format(self.appointment.subject_identifier,
                                      self.appointment.registered_subject.first_name,
                                      self.appointment.registered_subject.gender,
                                      self.appointment.visit_definition.code)

    @property
    def registered_subject(self):
        return self.get_registered_subject()

    class Meta(VisitModelMixin.Meta, RequiresConsentMixin.Meta):
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Visit"
        verbose_name_plural = "Clinic Visit"
        consent_model = 'bcpp_subject.clinicconsent'
