from edc_base.model_mixins import BaseUuidModel
from edc_visit_schedule.model_mixins import DisenrollmentModelMixin
from edc_consent.model_mixins import RequiresConsentMixin


class DisenrollmentClinic(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_clinic_admin'

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'clinic_visit_schedule.clinic_schedule'
        consent_model = 'bcpp_clinic.clinicconsent'
        app_label = 'bcpp_clinic
