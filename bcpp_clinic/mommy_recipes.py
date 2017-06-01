# coding=utf-8

from dateutil.relativedelta import relativedelta
from faker import Faker
from model_mommy.recipe import Recipe, seq

from edc_base_test.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES, FEMALE

from bcpp_clinic.models import ClinicEligibility


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
