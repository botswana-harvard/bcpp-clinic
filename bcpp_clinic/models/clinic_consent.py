from django.db import models

from simple_history.models import HistoricalRecords as AuditTrail
from registration.models import RegisteredSubject
from edc_consent.models.fields import (
    ReviewFieldsMixin, SampleCollectionFieldsMixin, PersonalFieldsMixin,
    CitizenFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin

from edc_consent.models import BaseConsent

from .clinic_off_study_mixin import ClinicOffStudyMixin


class ClinicConsent(PersonalFieldsMixin, VulnerabilityFieldsMixin, SampleCollectionFieldsMixin,
                    ReviewFieldsMixin, IdentityFieldsMixin, CitizenFieldsMixin, ClinicOffStudyMixin,
                    BaseConsent):
    """A model completed by the user to capture the ICF."""

    registered_subject = models.ForeignKey(RegisteredSubject, null=True)

    lab_identifier = models.CharField(
        verbose_name=("lab allocated identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
    )

    htc_identifier = models.CharField(
        verbose_name=("HTC Identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
    )

    pims_identifier = models.CharField(
        verbose_name=("PIMS identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
    )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        # self.clinic_subject_identifier()
        super(ClinicConsent, self).save(*args, **kwargs)

    def is_dispatchable_model(self):
        return False

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Consent RBD'
        verbose_name_plural = 'Clinic Consent RBD'
