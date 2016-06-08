from django.db import models

from edc_map.classes import site_mappers
from edc_base.audit_trail import AuditTrail
from edc.subject.registration.models import RegisteredSubject
from edc_consent.models.fields import (
    ReviewFieldsMixin, SampleCollectionFieldsMixin, PersonalFieldsMixin,
    CitizenFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin

from bhp066.apps.bcpp_subject.models.subject_consent import BaseBaseSubjectConsent
from bhp066.apps.bcpp_household_member.models import HouseholdMember

from .clinic_off_study_mixin import ClinicOffStudyMixin


class ClinicConsent(PersonalFieldsMixin, VulnerabilityFieldsMixin, SampleCollectionFieldsMixin,
                    ReviewFieldsMixin, IdentityFieldsMixin, CitizenFieldsMixin, ClinicOffStudyMixin,
                    BaseBaseSubjectConsent):
    """A model completed by the user to capture the ICF."""
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
        if not self.id:
            self.registered_subject = RegisteredSubject.objects.get(identity=self.identity)
            self.household_member = HouseholdMember.objects.get(registered_subject=self.registered_subject)
            self.survey = self.household_member.household_structure.survey
        self.community = site_mappers.current_community
        # self.clinic_subject_identifier()
        super(ClinicConsent, self).save(*args, **kwargs)

    def is_dispatchable_model(self):
        return False

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Consent RBD'
        verbose_name_plural = 'Clinic Consent RBD'
