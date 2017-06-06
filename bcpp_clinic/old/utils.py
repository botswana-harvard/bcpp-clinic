from django.apps import apps as django_apps

from edc_constants.constants import YES, ALIVE
from household.models.household_structure import HouseholdStructure
from plot.utils import get_clinic_n_anonymous_plot

from .constants import ABLE_TO_PARTICIPATE

from .models import ClinicHouseholdMember


def get_clinic_member(**options):
    current_survey_schedule = django_apps.get_app_config(
        'survey').current_survey_schedule
    plot_identifier = django_apps.get_app_config(
        'plot').clinic_plot_identifiers[0]
    plot_type = 'clinic'
    plot = get_clinic_n_anonymous_plot(
        plot_identifier=plot_identifier, plot_type=plot_type)
    household_structure = HouseholdStructure.objects.get(
        household__plot=plot,
        survey_schedule=current_survey_schedule)
    first_name = options.get('first_name')
    initials = options.get('initials')
    clinic_household_member = ClinicHouseholdMember.objects.create(
        household_structure=household_structure,
        gender=options.get('gender'),
        report_datetime=options.get('report_datetime'),
        age_in_years=options.get('age_in_years'),
        present_today=YES,
        survival_status=ALIVE,
        study_resident=YES,
        inability_to_participate=ABLE_TO_PARTICIPATE,
        relation='UNKNOWN',
        first_name=first_name,
        initials=initials,
        non_citizen=True,
    )
    return clinic_household_member
