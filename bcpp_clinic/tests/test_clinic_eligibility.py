from django.test import TestCase

from model_mommy import mommy
from bcpp_clinic.models import ClinicEligibility
from edc_map.site_mappers import site_mappers
from edc_map.mapper import Mapper


class TestPlotMapper(Mapper):

    map_area = 'test_community'
    map_code = '01'
    pair = 0
    landmarks = ()
    center_lat = -24.557709
    center_lon = 25.807963
    radius = 100.5
    location_boundary = ()
    intervention = True


site_mappers.register(TestPlotMapper)


class TestClinicEligibility(TestCase):

    def setUp(self):
        pass

    mommy.make_recipe('bcpp_clinic.cliniceligibility')
    self.assertEqual(ClinicEligibility.objects.all().count(), 1)
