from edc_base.model_mixins import BaseUuidModel
from edc_visit_schedule.model_mixins import DisenrollmentModelMixin

from ..managers import DisenrollmentManager

from .requires_consent_model_mixin import RequiresConsentMixin


class DisenrollmentClinic(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_clinic_admin'

    objects = DisenrollmentManager()

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'visit_schedule_clinic'
        consent_model = 'bcpp_clinic.clinicconsent'
        app_label = 'bcpp_clinic
