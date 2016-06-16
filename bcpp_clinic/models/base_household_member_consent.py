import re

from django.db import models

from edc_identifier.exceptions import IdentifierError
from edc_appointment.models import AppointmentMixin
from registration.models import RegisteredSubject
from edc_consent.models import BaseConsent
from edc_constants.choices import YES_NO

from ..choices import COMMUNITIES


class BaseClinicConsent(AppointmentMixin, BaseConsent):

    registered_subject = models.ForeignKey(
        RegisteredSubject,
        editable=False,
        null=True,
        help_text='one registered subject will be related to one household member for each survey')

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text=('Subject is a minor if aged 16-17. A guardian must be present for consent. '
                   'HIV status may NOT be revealed in the household.'))

    is_signed = models.BooleanField(default=False)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    def __unicode__(self):
        return '{0} ({1})'.format(self.subject_identifier, self.survey)

    def get_registration_datetime(self):
        return self.consent_datetime

    def save(self, *args, **kwargs):
        if not self.id:
            self.registered_subject = RegisteredSubject.objects.get(identity=self.identity)
        super(BaseHouseholdMemberConsent, self).save(*args, **kwargs)

    def _check_if_duplicate_subject_identifier(self, using):
        """Checks if the subject identifier is in use, for new and existing instances.

        .. warning:: this overrides default behavior!

        .. note:: overriding to change the constraint to subject_identifier + survey
                  instead of just subject_identifier."""
        if not self.pk and self.subject_identifier:
            if self.__class__.objects.using(using).filter(
                    subject_identifier=self.subject_identifier, survey=self.survey):
                obj = self.__class__.objects.using(using).filter(
                    subject_identifier=self.subject_identifier, survey=self.survey)
                raise IdentifierError('Attempt to insert duplicate value for '
                                      'subject_identifier {0} and survey {2} when '
                                      'saving {1} on add. See {3}.'.format(
                                          self.subject_identifier, self, self.survey, obj))
        else:
            if self.__class__.objects.using(using).filter(
                    subject_identifier=self.subject_identifier, survey=self.survey).exclude(pk=self.pk):
                obj = self.__class__.objects.using(using).filter(
                    subject_identifier=self.subject_identifier, survey=self.survey).exclude(pk=self.pk)
                raise IdentifierError('Attempt to insert duplicate value for '
                                      'subject_identifier {0} and survey {2} when '
                                      'saving {1} on change. See {3}.'.format(
                                          self.subject_identifier, self, self.survey, obj))
        self.check_for_duplicate_subject_identifier()

    def check_for_duplicate_subject_identifier(self):
        """Users may override to add an additional strategy to detect duplicate identifiers."""
        pass

    def post_save_update_registered_subject(self, using, **kwargs):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if re_pk.match(self.registered_subject.subject_identifier):
            self.registered_subject.subject_identifier = self.subject_identifier
        self.registered_subject.registration_status = 'CONSENTED'
        self.registered_subject.save(using=using)
        if self.subject_identifier != self.registered_subject.subject_identifier:
            raise TypeError('Subject identifier expected to be same as registered_subject '
                            'subject_identifier. Got {0} != {1}'.format(
                                self.subject_identifier, self.registered_subject.subject_identifier))

    def is_dispatchable_model(self):
        return False

    def deserialize_get_missing_fk(self, attrname):
        if attrname == 'household_member':
            registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
            survey = self.survey
            internal_identifier = registered_subject.registration_identifier
            household_member = self.household_member.__class__.objects.get(
                internal_identifier=internal_identifier,
                survey=survey)
            retval = household_member
        else:
            retval = None
        return retval

    class Meta:
        abstract = True
