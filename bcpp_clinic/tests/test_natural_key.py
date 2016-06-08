from django.core import serializers
from django.db.models import get_app, get_models
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc_base.encrypted_fields import FieldCryptor
from edc.device.sync.classes import SerializeToTransaction
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.appointment.models import Appointment
from edc.subject.registration.models import RegisteredSubject
from edc_map.classes import site_mappers

from bhp066.apps.bcpp_clinic.tests.factories import (
    ClinicEligibilityFactory, ClinicLocatorFactory, QuestionnaireFactory)
from bhp066.apps.bcpp_clinic.tests.factories import (ClinicConsentFactory, ClinicVisitFactory)
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from bhp066.apps.bcpp_clinic.models import ClinicEnrollmentLoss
from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_clinic.visit_schedule import BcppClinicVisitSchedule
from bhp066.apps.bcpp_lab.lab_profiles import ClinicSubjectProfile


class TestNaturalKey(TestCase):

    def setUp(self):
        site_mappers.autodiscover()
        try:
            site_lab_profiles.register(ClinicSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppClinicVisitSchedule().build()

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_clinic')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue(
                    'natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_clinic')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue(
                    'get_by_natural_key' in dir(model.objects),
                    'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        RegisteredSubject.objects.all().delete()
        instances = []
        self.assertEqual(ClinicEnrollmentLoss.objects.all().count(), 0)
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        clinic_eligibility = ClinicEligibilityFactory()
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        self.assertTrue(clinic_eligibility.is_eligible)
        clinic_eligibility.legal_marriage = 'No'
        clinic_eligibility.has_identity = 'No'
        clinic_eligibility.save()
        self.assertFalse(clinic_eligibility.is_eligible)
        self.assertEqual(ClinicEnrollmentLoss.objects.all().count(), 1)
        # clinic_loss = ClinicEnrollmentLoss.objects.all()[0]
        # instances.append(clinic_loss)
        clinic_eligibility.legal_marriage = 'Yes'
        clinic_eligibility.has_identity = 'Yes'
        clinic_eligibility.save()
        self.assertTrue(clinic_eligibility.is_eligible)
        instances.append(clinic_eligibility)
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        clinic_consent = ClinicConsentFactory(
            registered_subject=clinic_eligibility.household_member.registered_subject,
            identity=clinic_eligibility.identity,
            confirm_identity=clinic_eligibility.identity,
            dob=clinic_eligibility.dob,
            gender=clinic_eligibility.gender,
            first_name=clinic_eligibility.first_name,
            initials=clinic_eligibility.initials)
        self.assertEqual(Appointment.objects.all().count(), 1)
        instances.append(clinic_consent)
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        registered_subject = RegisteredSubject.objects.get(
            dob=clinic_eligibility.dob, gender=clinic_eligibility.gender,
            first_name=clinic_eligibility.first_name, initials=clinic_eligibility.initials)

        appointment = Appointment.objects.get(registered_subject=registered_subject)
        clinic_visit = ClinicVisitFactory(
            appointment=appointment, household_member=clinic_eligibility.household_member)
        instances.append(clinic_visit)
        clinic_subject_locator = ClinicLocatorFactory(clinic_visit=clinic_visit)
        instances.append(clinic_subject_locator)
        questionnaire = QuestionnaireFactory(clinic_visit=clinic_visit)
        instances.append(questionnaire)
#         clinic_eligibility.has_identity = 'No'
#         clinic_eligibility.save()
#         self.assertFalse(clinic_eligibility.is_eligible)

        for obj in instances:
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        # pp = pprint.PrettyPrinter(indent=4)
        for obj in instances:
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj, False, True, 'default')
            # print repr(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            de = serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in de:
                self.assertEqual(transaction.object.pk, obj.pk)
