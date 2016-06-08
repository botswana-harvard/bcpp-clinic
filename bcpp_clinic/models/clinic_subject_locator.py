from django.db import models

from edc.data_manager.models import TimePointStatusMixin
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.device.sync.models import BaseSyncUuidModel
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.export.managers import ExportHistoryManager
from edc.export.models import ExportTrackingFieldsMixin
from edc.subject.locator.models import BaseLocator
from edc_base.audit_trail import AuditTrail
from edc_base.bw.validators import BWCellNumber, BWTelephoneNumber
from edc_base.encrypted_fields import EncryptedCharField
from edc_consent.models import RequiresConsentMixin
from edc_constants.choices import YES_NO

from ..managers import ClinicModelManager

from .clinic_consent import ClinicConsent
from .clinic_off_study_mixin import ClinicOffStudyMixin
from .clinic_visit import ClinicVisit


class ClinicSubjectLocator(ExportTrackingFieldsMixin, ClinicOffStudyMixin, BaseLocator, RequiresConsentMixin,
                           TimePointStatusMixin, BaseDispatchSyncUuidModel, BaseSyncUuidModel):

    """A model completed by the user for locator data from consented participants."""

    CONSENT_MODEL = ClinicConsent

    clinic_visit = models.ForeignKey(ClinicVisit)

    alt_contact_cell_number = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
    )
    has_alt_contact = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="If we are unable to contact the person indicated above, is there another"
                     " individual (including next of kin) with whom the study team can get"
                     " in contact with?",
        help_text="",
    )

    alt_contact_name = EncryptedCharField(
        max_length=35,
        verbose_name="Full Name of the responsible person",
        help_text="include first name and surname",
        blank=True,
        null=True,
    )

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

    export_history = ExportHistoryManager()

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(ClinicVisit)

    objects = ClinicModelManager()

    def save(self, *args, **kwargs):
        if self.clinic_visit:
            if not self.registered_subject:
                self.registered_subject = self.clinic_visit.appointment.registered_subject
        super(ClinicSubjectLocator, self).save(*args, **kwargs)

    def natural_key(self):
        return self.clinic_visit.natural_key()

    def get_visit(self):
        return self.clinic_visit

    def get_subject_identifier(self):
        if self.get_visit():
            return self.get_visit().get_subject_identifier()
        return None

    def get_report_datetime(self):
        return self.created

    def __unicode__(self):
        return unicode(self.clinic_visit)

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = "Clinic Subject Locator"
        verbose_name_plural = "Clinic Subject Locator"
