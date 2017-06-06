from django.test import TestCase, tag

from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_constants.constants import MALE

from ..models import ClinicEligibility
from ..utils import get_clinic_member


@tag('TestCreateClinicEligibility')
class TestCreateClinicEligibility(TestCase):

    def setUp(self):
        pass

    @tag('eligibility_creation')
    def test_clinic_eligibility(self):
        """Test create clinic eligibilty.
        """
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
        self.assertEqual(ClinicEligibility.objects.all().count(), 1)

    def test_create_two_clinic_eligibility(self):
        """Test create 2 clinic eligibilty.
        """
        options = {}
        options.update(
            first_name='TEST1',
            initials='TT',
            report_datetime=get_utcnow(),
            age_in_years=22,
            gender=MALE)
        clinic_household_member_one = get_clinic_member(**options)
        options.update(first_name='TEST2')
        clinic_household_member_two = get_clinic_member(**options)

        mommy.make_recipe(
            'bcpp_clinic.cliniceligibility',
            clinic_household_member=clinic_household_member_one)
        mommy.make_recipe(
            'bcpp_clinic.cliniceligibility',
            clinic_household_member=clinic_household_member_two)

        self.assertEqual(ClinicEligibility.objects.all().count(), 2)
