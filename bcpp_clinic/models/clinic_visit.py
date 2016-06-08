from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_constants.constants import NEW
from edc.entry_meta_data.models import RequisitionMetaData, ScheduledEntryMetaData
from edc.lab.lab_clinic_api.models import Panel
from edc.subject.entry.models import LabEntry, Entry
from edc.subject.visit_tracking.models import BaseVisitTracking
from edc_consent.models import RequiresConsentMixin
from edc.device.sync.models import BaseSyncUuidModel

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from .clinic_off_study_mixin import ClinicOffStudyMixin
from .clinic_consent import ClinicConsent


class ClinicVisit(ClinicOffStudyMixin, RequiresConsentMixin, BaseVisitTracking, BaseSyncUuidModel):
    """A model completed by the user to indicate track the actual appointment or visit.

    The model captures actual report date, time and location (home, clinic, etc)."""

    CONSENT_MODEL = ClinicConsent

    household_member = models.ForeignKey(HouseholdMember)

    reason_unscheduled = models.CharField(
        verbose_name="If 'Unscheduled' above, provide reason for the unscheduled visit",
        max_length=25,
        blank=True,
        null=True,
    )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.info_source = 'subject'
        self.reason = 'clinic RBD'
        self.appointment.appt_type = 'clinic'
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        super(ClinicVisit, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} {} ({}) {}'.format(self.appointment.registered_subject.subject_identifier,
                                      self.appointment.registered_subject.first_name,
                                      self.appointment.registered_subject.gender,
                                      self.appointment.visit_definition.code)

    @property
    def registered_subject(self):
        return self.get_registered_subject()

    def dispatch_container_lookup(self):
        return (('bcpp_household', 'Plot'), 'household_member__household_structure__household__plot__plot_identifier')

    def get_requisition(self):
        """Confirms the visit code and visit reason before
        updating the VL requisition metadata status to NEW."""
        lab_model = ['clinicrequisition']
        check_consent = ClinicConsent.objects.filter(
            subject_identifier=self.registered_subject.subject_identifier)
        if check_consent[0]:
            if self.appointment.visit_definition.code == 'C0':
                if self.reason in ['Initiation Visit', 'Other NON-VL Visit']:
                    for lab in lab_model:
                        panel = Panel.objects.get(edc_name='Viral Load (clinic)')
                        lab_entry = LabEntry.objects.filter(
                            model_name=lab,
                            requisition_panel_id=panel.id,
                            visit_definition_id=self.appointment.visit_definition_id)
                        if lab_entry:
                            requisition_meta_data = RequisitionMetaData.objects.filter(
                                appointment=self.appointment,
                                lab_entry=lab_entry[0],
                                registered_subject=self.registered_subject)
                            if not requisition_meta_data:
                                requisition_meta_data = RequisitionMetaData.objects.create(
                                    appointment=self.appointment,
                                    lab_entry=lab_entry[0],
                                    registered_subject=self.registered_subject)
                            else:
                                requisition_meta_data = requisition_meta_data[0]
                            requisition_meta_data.entry_status = NEW
                            requisition_meta_data.save()

    def ccc_masa_visit_reason_forms(self):
        """Confirms the visit code and visit reason before
        updating the VL tracking scheduled metadata status to NEW."""
        if self.appointment.visit_definition.code == 'C0':
            if self.reason in ['MASA Scheduled VL Visit', 'CCC visit']:
                entry = Entry.objects.get(
                    model_name='viralloadtracking',
                    visit_definition_id=self.appointment.visit_definition_id)
                scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                    appointment=self.appointment,
                    entry=entry,
                    registered_subject=self.registered_subject)
                if not scheduled_meta_data:
                    scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                        appointment=self.appointment,
                        entry=entry,
                        registered_subject=self.registered_subject)
                else:
                    scheduled_meta_data = scheduled_meta_data[0]
                scheduled_meta_data.entry_status = NEW
                scheduled_meta_data.save()
                return scheduled_meta_data

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Visit"
        verbose_name_plural = "Clinic Visit"
