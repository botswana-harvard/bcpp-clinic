# coding=utf-8

from dateutil.relativedelta import relativedelta
from faker import Faker
from model_mommy.recipe import Recipe, seq

from edc_base_test.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES, FEMALE, ALIVE

from .constants import ABLE_TO_PARTICIPATE
from .models import ClinicEligibility, ClinicHouseholdMember


fake = Faker()

cliniceligibility = Recipe(
    ClinicEligibility,
    report_datetime=get_utcnow,
    dob=(get_utcnow() - relativedelta(years=25)).date(),
    part_time_resident=YES,
    initials='EW',
    gender=FEMALE,
    household_residency=YES,
    has_identity=YES,
    identity=seq('12315678'),
    confirm_identity=seq('12315678'),
    identity_type='OMANG',
    citizen=YES,
    literacy=YES,
    guardian=NOT_APPLICABLE,
    confirm_participation=NOT_APPLICABLE,
)

clinichouseholdmember = Recipe(
    ClinicHouseholdMember,
    report_datetime=get_utcnow,
    first_name=fake.first_name,
    initials='XX',
    inability_to_participate=ABLE_TO_PARTICIPATE,
    survival_status=ALIVE,
    age_in_years=25,
    study_resident=YES,
    gender=FEMALE,
    relation='cousin',
    subject_identifier=None,
    subject_identifier_as_pk=None,
    subject_identifier_aka=None,
    internal_identifier=None,
)
