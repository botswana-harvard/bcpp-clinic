from datetime import datetime, date
from uuid import uuid4

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.conf import settings
from django.test.utils import override_settings

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc_constants.constants import NOT_APPLICABLE
from edc.core.bhp_variables.models import StudySite
from edc.subject.registration.models import RegisteredSubject
from edc_map.classes import site_mappers

from bhp066.apps.bcpp.app_configuration.classes import bcpp_app_configuration
from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, HouseholdFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_survey.models import Survey

from ..models import ClinicEligibility
from .factories import ClinicConsentFactory


class TestClinicEligibility(TestCase):

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def setUp(self):
        site_mappers.autodiscover()
        from edc.subject.visit_schedule.classes import site_visit_schedules
        self.household_member = None
        self.subject_consent = None
        self.registered_subject = None
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        bcpp_app_configuration.prepare()
        site_lab_tracker.autodiscover()
        site_visit_schedules.autodiscover()
        site_visit_schedules.build_all()

        self.survey = Survey.objects.current_survey()
        self.plot = PlotFactory(community=settings.CURRENT_COMMUNITY, household_count=1, status='bcpp_clinic')
        self.household = HouseholdFactory(plot=self.plot)
        self.household_structure = HouseholdStructure.objects.get(household=self.household, survey=self.survey)
        self.study_site = StudySite.objects.get(
            site_code=site_mappers.get_mapper(site_mappers.current_community).map_code)
        self.intervention = site_mappers.get_mapper(site_mappers.current_community).intervention
        # site_mappers().get_mapper(site_mappers.current_community).verify_survey_dates()

    def test_additional_key_similar_eligibility_member_subject(self):
        """Tests constraint across hhm, clinic_eligibility and registered_subject
        unique_together = ['first_name', 'initials', 'identity', 'additional_key']"""
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='ERIK',
            initials='EW',
            age_in_years=50,
            identity=None,
            identity_type='OMANG',
        )
        clinic_eligibility.save()
        self.assertIsInstance(clinic_eligibility.additional_key, uuid4().__class__)
        self.assertEquals(clinic_eligibility.additional_key, clinic_eligibility.household_member.additional_key)
        self.assertEquals(
            clinic_eligibility.additional_key, clinic_eligibility.household_member.registered_subject.additional_key)

    def test_consent_updating_subject(self):
        """Tests that after consent, subject identifier is created and registered subject is properly updated."""
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1964, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        clinic_eligibility.save()

        clinic_eligibility = ClinicEligibility.objects.get(pk=clinic_eligibility.pk)

        self.assertEqual(clinic_eligibility.household_member.registered_subject.identity, clinic_eligibility.identity)

        clinic_consent = ClinicConsentFactory(
            household_member=clinic_eligibility.household_member,
            gender='F',
            dob=clinic_eligibility.dob,
            first_name='SUE',
            last_name='W',
            citizen='Yes',
            identity='111121112',
            identity_type='OMANG',
            confirm_identity='111121112',
            initials=clinic_eligibility.initials,
            study_site=self.study_site)

        initial_identifier = clinic_consent.subject_identifier
        self.assertEqual(RegisteredSubject.objects.filter(
            subject_identifier=clinic_consent.subject_identifier).count(), 1)
        clinic_consent.save()
        self.assertEqual(initial_identifier, clinic_consent.subject_identifier)

    def test_cannot_save_eligibility_when_consented(self):
        """Assert that eligibility will not save if subject already consented."""
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1964, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        clinic_eligibility.save()

        clinic_eligibility = ClinicEligibility.objects.get(pk=clinic_eligibility.pk)

        ClinicConsentFactory(
            household_member=clinic_eligibility.household_member,
            gender='F',
            dob=clinic_eligibility.dob,
            first_name='SUE',
            last_name='W',
            citizen='Yes',
            identity='111121112',
            identity_type='OMANG',
            confirm_identity='111121112',
            initials=clinic_eligibility.initials,
            study_site=self.study_site)

        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1964, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        with self.assertRaises(ValidationError):
            clinic_eligibility.save()

    def test_age_reason_lt_16(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(2000, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        clinic_eligibility.save()
        self.assertEqual('Too young (<16).', clinic_eligibility.age_reason([])[0])

    def test_age_reason_lt_16_ineligible(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(2000, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        clinic_eligibility.save()
        self.assertEqual('Minor.', clinic_eligibility.age_reason_ineligible([])[0])

    def test_age_reason_gt_64(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1940, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        clinic_eligibility.save()
        self.assertEqual('Too old (>64).', clinic_eligibility.age_reason([])[0])

    def test_age_reason_gt_64_ineligible(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1940, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
        )
        clinic_eligibility.save()
        self.assertEqual('Too old.', clinic_eligibility.age_reason_ineligible([])[0])

    def test_literacy_reason(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1940, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
            literacy='No'
        )
        self.assertEqual('Illiterate with no literate witness.', clinic_eligibility.literacy_reason([])[0])

    def test_literacy_reason_unknown(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1949, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
            literacy='Unknown'
        )
        self.assertEqual('Literacy unknown.', clinic_eligibility.literacy_reason([])[0])

    def test_hiv_status_reason_neg(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1940, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
            literacy='Unknown',
            hiv_status='NEG'
        )
        self.assertEqual('HIV Negative.', clinic_eligibility.hiv_status_reason([])[0])

    def test_hiv_status_reason_unknown(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1940, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
            literacy='Unknown',
            hiv_status='unknown'
        )
        self.assertEqual('HIV status unknown.', clinic_eligibility.hiv_status_reason([])[0])

    def test_part_time_resident_reason(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1940, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
            literacy='Unknown',
            hiv_status='unknown',
            part_time_resident='No'
        )
        self.assertEqual('Not resident.', clinic_eligibility.part_time_resident_reason([])[0])

    def test_part_time_resident_reason_unk(self):
        clinic_eligibility = ClinicEligibility(
            report_datetime=datetime.today(),
            first_name='SUE',
            initials='SW',
            dob=date(1940, 5, 27),
            identity='111121112',
            identity_type='OMANG',
            gender='F',
            literacy='Unknown',
            hiv_status='unknown',
            part_time_resident='Unknown'
        )
        self.assertEqual('Residency unknown.', clinic_eligibility.part_time_resident_reason([])[0])
