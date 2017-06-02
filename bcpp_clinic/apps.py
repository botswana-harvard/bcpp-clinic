from django.apps import AppConfig as DjangoApponfig

from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_visit_tracking.constants import SCHEDULED, LOST_VISIT
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig


class AppConfig(DjangoApponfig):
    name = 'bcpp_clinic'
    listboard_template_name = 'bcpp_clinic/listboard.html'
    dashboard_template_name = 'bcpp_clinic/dashboard.html'
    base_template_name = 'edc_base/base.html'
    listboard_url_name = 'bcpp_clinic:listboard_url'
    dashboard_url_name = 'bcpp_clinic:dashboard_url'
    admin_site_name = 'bcpp_clinic_admin'


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {'bcpp_clinic.clnictvisit': 'reason'}
    create_on_reasons = [SCHEDULED]
    delete_on_reasons = [LOST_VISIT, FAILED_ELIGIBILITY]
    metadata_rules_enabled = True  # default


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        'bcpp_clinic': ('clinic_visit', 'bcpp_clinic.clinicvisit')}
