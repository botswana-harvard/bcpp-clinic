from django.test import TestCase

from model_mommy import mommy
from bcpp_clinic.models.clinic_eligibility import ClinicEligibility


class TestClinicEligibility(TestCase):

    def setUp(self):
        pass

    def test_clinic_eligibility(self):
        mommy.make_recipe('bcpp_clinic.cliniceligibility')
        self.assertEqual(ClinicEligibility.objects.all().count(), 1)
