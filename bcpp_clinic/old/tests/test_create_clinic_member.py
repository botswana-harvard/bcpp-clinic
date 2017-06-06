from django.test import TestCase

from edc_constants.constants import MALE
from edc_base.utils import get_utcnow
from bcpp_clinic.utils import get_clinic_member
from ..models import ClinicHouseholdMember


class TestCreateClinicMember(TestCase):

    def setUp(self):
        pass

    def test_create_clinic_member(self):
        options = {}
        options.update(
            first_name='TEST',
            initials='TT',
            report_datetime=get_utcnow(),
            age_in_years=22,
            gender=MALE)
        get_clinic_member(**options)
        self.assertEqual(ClinicHouseholdMember.objects.all().count(), 1)
