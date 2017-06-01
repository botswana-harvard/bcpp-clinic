from django.db import models

from edc_consent.model_mixins import ConsentModelMixin
from survey.model_mixins import SurveyScheduleModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_consent.field_mixins.review_fields_mixin import ReviewFieldsMixin
from edc_consent.field_mixins.bw.identity_fields_mixin import IdentityFieldsMixin
from edc_consent.field_mixins.personal_fields_mixin import PersonalFieldsMixin
from edc_consent.field_mixins.citizen_fields_mixin import CitizenFieldsMixin
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_consent.field_mixins.vulnerability_fields_mixin import VulnerabilityFieldsMixin
from edc_consent.field_mixins.sample_collection_fields_mixin import SampleCollectionFieldsMixin
from member.models.household_member.household_member import HouseholdMember
from edc_constants.choices import YES_NO
from edc_registration.model_mixins.updates_or_creates_registered_subject_model_mixin import UpdatesOrCreatesRegistrationModelMixin
from edc_dashboard.model_mixins import SearchSlugModelMixin


class ClinicConsent(ConsentModelMixin, UpdatesOrCreatesRegistrationModelMixin,
                    NonUniqueSubjectIdentifierModelMixin,
                    SurveyScheduleModelMixin, IdentityFieldsMixin,
                    ReviewFieldsMixin, PersonalFieldsMixin,
                    SampleCollectionFieldsMixin, CitizenFieldsMixin,
                    VulnerabilityFieldsMixin, SearchSlugModelMixin,
                    BaseUuidModel):
    """ A model completed by the user that captures the ICF.
    """

    household_member = models.ForeignKey(
        HouseholdMember, on_delete=models.PROTECT)

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text=('Subject is a minor if aged 16-17. A guardian must '
                   'be present for consent. HIV status may NOT be '
                   'revealed in the household.'),
        editable=False)

    is_signed = models.BooleanField(
        default=False,
        editable=False)

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

    def __str__(self):
        return '{0} ({1}) V{2}'.format(
            self.subject_identifier,
            self.survey_schedule_object.name,
            self.version)

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Consent RBD'
        verbose_name_plural = 'Clinic Consent RBD'
        ordering = ('-created', )
