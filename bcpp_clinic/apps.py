import os

from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz

from django.apps import AppConfig as DjangoApponfig
from django.conf import settings

from bcpp_clinic_subject.constants import CLINIC_RBD
from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_appointment.facility import Facility
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_base.utils import get_utcnow
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
from edc_label.apps import AppConfig as BaseEdcLabelAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig, SubjectType, Cap
from edc_sync.apps import AppConfig as BaseEdcSyncAppConfig
from edc_sync_files.apps import AppConfig as BaseEdcSyncFilesAppConfig
from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
from edc_timepoint.timepoint import Timepoint
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from .navbars import navbars


class AppConfig(DjangoApponfig):
    name = 'bcpp_clinic'
    listboard_template_name = 'bcpp_clinic/listboard.html'
    dashboard_template_name = 'bcpp_clinic/dashboard.html'
    base_template_name = 'bcpp_clinic/base.html'
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
    protocol_name = 'BCPP Clinic'
    protocol_title = 'Botswana Combination Prevention Project'
    subject_types = [
        SubjectType('subject', 'Research Subject',
                    Cap(model_name='bcpp_clinic_subject.subjectconsent', max_subjects=9999)),
    ]
    study_open_datetime = datetime(2013, 10, 18, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))

    @property
    def site_name(self):
        return 'test_community'

    @property
    def site_code(self):
        return '01'


class EdcLabAppConfig(BaseEdcLabAppConfig):
    base_template_name = 'bcpp_clinic/base.html'
    requisition_model = 'bcpp_clinic_subject.subjectrequisition'
    result_model = 'edc_lab.result'

    @property
    def study_site_name(self):
        return 'test_community'


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {'bcpp_clinic_subject.subjectvisit': 'reason'}
    create_on_reasons = [CLINIC_RBD, SCHEDULED, UNSCHEDULED]
    delete_on_reasons = [LOST_VISIT, FAILED_ELIGIBILITY]
    metadata_rules_enabled = True  # default


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        'bcpp_clinic_subject': ('subject_visit', 'bcpp_clinic_subject.subjectvisit')}


class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
    timepoints = [
        Timepoint(
            model='bcpp_clinic_subject.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
        Timepoint(
            model='bcpp_clinic_subject.historicalappointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
    ]


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    app_label = 'bcpp_clinic_subject'
    default_appt_type = 'clinic'
    facilities = {
        'clinic': Facility(name='clinic', days=[MO, TU, WE, TH, FR, SA, SU],
                           slots=[99999, 99999, 99999, 99999, 99999, 99999, 99999])}


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Bcpp Clinic'
    institution = 'Botswana-Harvard AIDS Institute'
    copyright = '2013-{}'.format(get_utcnow().year)
    license = None

    def get_navbars(self):
        return navbars


class EdcSyncAppConfig(BaseEdcSyncAppConfig):
    edc_sync_files_using = True
    role = CENTRAL_SERVER


class EdcSyncFilesAppConfig(BaseEdcSyncFilesAppConfig):
    edc_sync_files_using = True
    role = CENTRAL_SERVER


class EdcLabelAppConfig(BaseEdcLabelAppConfig):
    template_folder = os.path.join(
        settings.STATIC_ROOT, 'bcpp_clinic', 'label_templates')
