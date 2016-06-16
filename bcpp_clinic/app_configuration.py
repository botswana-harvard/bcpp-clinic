from datetime import datetime, date

from edc_lab.lab_packing.models import DestinationTuple
from edc_lab.lab_profile.classes import ProfileItemTuple, ProfileTuple
from edc_configuration.base_app_configuration import BaseAppConfiguration
from edc_device import Device

from lis.labeling.classes import LabelPrinterTuple, ZplTemplateTuple, ClientTuple
from lis.specimen.lab_aliquot_list.classes import AliquotTypeTuple
from lis.specimen.lab_panel.classes import PanelTuple

from .constants import MIN_AGE_OF_CONSENT

try:
    from config.labels import aliquot_label
except ImportError:
    aliquot_label = None

study_start_datetime = datetime(2016, 4, 1, 0, 0, 0)
study_end_datetime = datetime(2016, 12, 1, 0, 0, 0)


class AppConfiguration(BaseAppConfiguration):

    global_configuration = {
        'dashboard':
            {'show_not_required': True,
             'allow_additional_requisitions': False,
             'show_drop_down_requisitions': True},
        'appointment':
            {'allowed_iso_weekdays': ('12345', False),
             'use_same_weekday': True,
             'default_appt_type': 'clinic',
             'appointments_per_day_max': 20,
             'appointments_days_forward': 15},
        'protocol': {
            'start_datetime': study_start_datetime,
            'end_datetime': study_end_datetime},
    }

    study_variables_setup = {
        'protocol_number': 'BHP085',
        'protocol_code': '085',
        'protocol_title': 'BHP085',
        'research_title': 'Tshilo Dikotla',
        'study_start_datetime': study_start_datetime,
        'minimum_age_of_consent': MIN_AGE_OF_CONSENT,
        'maximum_age_of_consent': 50,
        'gender_of_consent': 'F',
        'subject_identifier_seed': '10000',
        'subject_identifier_prefix': '000',
        'subject_identifier_modulus': '7',
        'subject_type': 'subject',
        'machine_type': 'SERVER',
        'hostname_prefix': '0000',
        'device_id': Device().device_id}

    holidays_setup = {
        'New Year': date(2016, 1, 1),
        'New Year Holiday': date(2016, 1, 2),
        'Good Friday': date(2016, 3, 25),
        'Easter Monday': date(2016, 3, 28),
        'Labour Day': date(2016, 5, 1),
        'Labour Day Holiday': date(2016, 5, 2),
        'Ascension Day': date(2016, 5, 5),
        'Sir Seretse Khama Day': date(2016, 7, 1),
        'President\'s Day': date(2016, 7, 18),
        'President\'s Day Holiday': date(2016, 7, 19),
        'Independence Day': date(2016, 9, 30),
        'Botswana Day Holiday': date(2016, 10, 1),
        'Christmas Day': date(2016, 12, 25),
        'Boxing Day': date(2016, 12, 26)}

    consent_type_setup = [
        {'app_label': 'td_maternal',
         'model_name': 'maternalconsent',
         'start_datetime': study_start_datetime,
         'end_datetime': datetime(2016, 12, 31, 23, 59),
         'version': '1'}
    ]

    study_site_setup = []

    lab_clinic_api_setup = {
        'panel': [PanelTuple('CD4', 'TEST', 'WB'),
                  PanelTuple('Viral Load', 'TEST', 'WB'),
                  PanelTuple('Fasting Glucose', 'TEST', 'WB'),
                  PanelTuple('Glucose 1h', 'TEST', 'WB'),
                  PanelTuple('Glucose 2h', 'TEST', 'WB')],
        'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                         AliquotTypeTuple('Glucose', 'GLUC', '03'),
                         AliquotTypeTuple('Plasma', 'PL', '32'),
                         AliquotTypeTuple('Buffy Coat', 'BC', '16'),]}

    lab_setup = {'tshilo_dikotla': {
                 'destination': [DestinationTuple('BHHRL', 'Botswana-Harvard HIV Reference Laboratory',
                                                  'Gaborone', '3902671', 'bhhrl@bhp.org.bw')],
                 'panel': [PanelTuple('CD4', 'TEST', 'WB'),
                           PanelTuple('Viral Load', 'TEST', 'WB'),
                           PanelTuple('Fasting Glucose', 'TEST', 'WB'),
                           PanelTuple('Glucose 1h', 'TEST', 'WB'),
                           PanelTuple('Glucose 2h', 'TEST', 'WB')],
                 'aliquot_type': [AliquotTypeTuple('Whole Blood', 'WB', '02'),
                                  AliquotTypeTuple('Plasma', 'PL', '32'),
                                  AliquotTypeTuple('Buffy Coat', 'BC', '16'),
                                  AliquotTypeTuple('Glucose', 'GLUC', '03')],
                 'profile': [ProfileTuple('Viral Load', 'WB'),
                             ProfileTuple('Glucose', 'GLUC')],
                 'profile_item': [ProfileItemTuple('Viral Load', 'PL', 1.0, 3),
                                  ProfileItemTuple('Viral Load', 'BC', 0.5, 1),
                                  ProfileItemTuple('Glucose', 'GLUC', 1, 1)]}}
    labeling_setup = {}
