from django.test import TestCase

from model_mommy import mommy

from faker import Faker

from member.tests.mixins import MemberMixin
from edc_constants.constants import MALE
from ..models import ClinicEligibility
from edc_base.utils import get_utcnow
from bcpp_clinic.utils import get_clinic_member

fake = Faker()


class TestClinicEligibility(MemberMixin, TestCase):

    def setUp(self):
        pass

    def test_clinic_eligibility(self):
#         options = {}
#         options.update(
#             first_name='TEST',
#             initials='TT',
#             report_datetime=get_utcnow(),
#             age_in_years=22,
#             gender=MALE)
#         clinic_household_member = get_clinic_member(**options)
        mommy.make_recipe(
            'bcpp_clinic.cliniceligibility')
        self.assertEqual(ClinicEligibility.objects.all().count(), 1)
