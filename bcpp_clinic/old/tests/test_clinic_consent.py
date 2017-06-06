from model_mommy import mommy

from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import MALE

from ..utils import get_clinic_member
from ..models import ClinicConsent, ClinicHouseholdMember


class TestClinicConsent(TestCase):

    def setUp(self):
        pass

    def test_consent_updates_member_status(self):
        options = {}
        options.update(
            first_name='TEST',
            initials='TT',
            report_datetime=get_utcnow(),
            age_in_years=22,
            gender=MALE)
        clinic_household_member = get_clinic_member(**options)
        mommy.make_recipe(
            'bcpp_clinic.cliniceligibility',
            clinic_household_member=clinic_household_member)
        clinic_consent = mommy.make_recipe(
            'bcpp_clinic.clinicconsent',
            clinic_household_member=clinic_household_member)
        clinic_household_memnber = ClinicHouseholdMember.objects.get(
            id=clinic_consent.clinic_household_memnber.id)
        self.assertTrue(clinic_household_memnber.household_structure.enrolled)
        self.assertEqual(ClinicConsent.objects.all().count(), 1)
