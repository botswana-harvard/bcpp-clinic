from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model_mixins import BaseUuidModel
from edc_dashboard.model_mixins import SearchSlugManager, SearchSlugModelMixin
from edc_lab.model_mixins.requisition import (
    RequisitionModelMixin, RequisitionStatusMixin, RequisitionIdentifierMixin)
from edc_metadata.model_mixins.updates import UpdatesRequisitionMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import (
    CrfModelManager as VisitTrackingCrfModelManager)
from edc_visit_tracking.model_mixins import (
    CrfModelMixin as VisitTrackingCrfModelMixin, PreviousVisitModelMixin)

from edc_map.site_mappers import site_mappers
from edc_consent.model_mixins import RequiresConsentMixin

from ..models import ClinicVisit


class Manager(VisitTrackingCrfModelManager, SearchSlugManager):
    pass


class ClinicRequisition(
        RequisitionModelMixin, RequisitionStatusMixin, RequisitionIdentifierMixin,
        VisitTrackingCrfModelMixin, OffstudyMixin,
        RequiresConsentMixin, PreviousVisitModelMixin,
        UpdatesRequisitionMetadataModelMixin, SearchSlugModelMixin,
        BaseUuidModel):

    clinic_visit = models.ForeignKey(ClinicVisit, on_delete=PROTECT)

    objects = Manager()

    def save(self, *args, **kwargs):
        self.study_site = site_mappers.current_map_code
        self.study_site_name = site_mappers.current_map_area
        super().save(*args, **kwargs)

    def get_slugs(self):
        return ([self.subject_visit.subject_identifier,
                 self.requisition_identifier,
                 self.human_readable_identifier,
                 self.panel_name,
                 self.panel_object.abbreviation,
                 self.identifier_prefix]
                + self.subject_visit.household_member.get_slugs())

    class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
        consent_model = 'bcpp_clinic.clinicconsent'
        app_label = 'bcpp_clinic'
