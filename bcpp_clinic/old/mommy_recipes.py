# coding=utf-8

from dateutil.relativedelta import relativedelta
from faker import Faker
from model_mommy.recipe import Recipe, seq

from edc_base_test.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES, ALIVE, POS,\
    MALE
from member.constants import ABLE_TO_PARTICIPATE

from .models import ClinicEligibility, ClinicHouseholdMember, ClinicConsent


fake = Faker()

cliniceligibility = Recipe(
    ClinicEligibility,
    report_datetime=get_utcnow,
    dob=(get_utcnow() - relativedelta(years=25)).date(),
    part_time_resident=YES,
    initials='TT',
    gender=MALE,
    has_identity=YES,
    hiv_status=POS,
    identity=seq('12315678'),
    confirm_identity=seq('12315678'),
    identity_type='OMANG',
    inability_to_participate=ABLE_TO_PARTICIPATE,
    citizen=YES,
    literacy=YES,
    guardian=NOT_APPLICABLE,
)

clinichouseholdmember = Recipe(
    ClinicHouseholdMember,
    report_datetime=get_utcnow,
    first_name=fake.first_name,
    initials='TT',
    inability_to_participate=ABLE_TO_PARTICIPATE,
    survival_status=ALIVE,
    age_in_years=25,
    study_resident=YES,
    gender=MALE,
    relation='cousin',
    subject_identifier=None,
    subject_identifier_as_pk=None,
    subject_identifier_aka=None,
    internal_identifier=None,
)

clinicconsent = Recipe(
    ClinicConsent,
    consent_datetime=get_utcnow,
    citizen=YES,
    confirm_identity=seq('12315678'),
    dob=(get_utcnow() - relativedelta(years=25)).date(),
    gender=MALE,
    identity=seq('12315678'),
    identity_type='OMANG',
    initials='TT',
    is_literate=YES,
    study_site=12,
    guardian_name=None,
    is_signed=True,
    is_verified=True,
    may_store_samples=YES,
    subject_identifier=None,
)
