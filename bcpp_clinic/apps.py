from django.apps import AppConfig as DjangoApponfig
from django.conf import settings

from datetime import datetime
from dateutil.tz import gettz


from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig, SubjectType, Cap


class AppConfig(DjangoApponfig):
    name = 'bcpp_clinic'
    listboard_template_name = 'bcpp_clinic/listboard.html'
    dashboard_template_name = 'bcpp_clinic/dashboard.html'
    base_template_name = 'edc_base/base.html'
    listboard_url_name = 'bcpp_clinic:listboard_url'
    dashboard_url_name = 'bcpp_clinic:dashboard_url'
    admin_site_name = 'bcpp_clinic_admin'
    eligibility_age_adult_lower = 16
    eligibility_age_adult_upper = 64


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = '066'


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    use_settings = True
    device_id = settings.DEVICE_ID
    device_role = settings.DEVICE_ROLE


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP066'
    protocol_number = '066'
    protocol_name = 'BCPP'
    protocol_title = 'Botswana Combination Prevention Project'
    subject_types = [
        SubjectType('clinic', 'Research Subject',
                    Cap(model_name='bcpp_clinic.clinicconsent', max_subjects=9999)),
    ]
    study_open_datetime = datetime(2013, 10, 18, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))

    @property
    def site_name(self):
        from edc_map.site_mappers import site_mappers
        return site_mappers.current_map_area

    @property
    def site_code(self):
        from edc_map.site_mappers import site_mappers
        return site_mappers.current_map_code
