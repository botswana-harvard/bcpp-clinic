from django.db import models

from edc_locator.model_mixins import LocatorModelMixin
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from django_crypto_fields.fields.encrypted_char_field import EncryptedCharField
from edc_base.model_validators.bw.validators import BWCellNumber,\
    BWTelephoneNumber
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_consent.model_mixins import RequiresConsentMixin


class ClinicSubjectLocator(LocatorModelMixin, RequiresConsentMixin, BaseUuidModel):
    """A model completed by the user to that captures participant
    locator information and permission to contact.
    """

    alt_contact_cell_number = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True)

    has_alt_contact = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        verbose_name=(
            'If we are unable to contact the person indicated above, '
            'is there another individual (including next of kin) with '
            'whom the study team can get in contact with?'))

    alt_contact_name = EncryptedCharField(
        max_length=35,
        verbose_name="Full Name of the responsible person",
        help_text="include first name and surname",
        blank=True,
        null=True)

    alt_contact_rel = EncryptedCharField(
        max_length=35,
        verbose_name="Relationship to participant",
        blank=True,
        null=True,
        help_text="",
    )
    alt_contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
    )

    other_alt_contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
    )

    alt_contact_tel = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone number",
        validators=[BWTelephoneNumber, ],
        help_text="",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.clinic_visit

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = "Clinic Subject Locator"
        verbose_name_plural = "Clinic Subject Locator"
