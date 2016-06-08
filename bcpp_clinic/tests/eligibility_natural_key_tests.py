# from django.core import serializers
# from django.db.models import get_app, get_models
# from django.test import TestCase
#
# from edc.lab.lab_profile.classes import site_lab_profiles
# from edc.core.crypto_fields.classes import FieldCryptor
# from edc.device.sync.classes import SerializeToTransaction
# from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
# from edc.subject.lab_tracker.classes import site_lab_tracker
# from edc.subject.appointment.models import Appointment
# from edc.subject.registration.models import RegisteredSubject
#
# from .factories import (ClinicEligibilityFactory, ClinicEnrollmentLossFactory)
# from bhp066.apps.bcpp_clinic.visit_schedule import BcppClinicVisitSchedule
# from bhp066.apps.bcpp_clinic.lab_profiles import ClinicSubjectProfile
#
#
# class EligibilityNaturalKeyTests(TestCase):
#
#     def setUp(self):
#         try:
#             site_lab_profiles.register(ClinicSubjectProfile())
#         except AlreadyRegisteredLabProfile:
#             pass
#         BcppClinicConfiguration()
#         site_lab_tracker.autodiscover()
#         BcppClinicVisitSchedule().build()
#
#     def test_p1(self):
#         """Confirms all models have a natural_key method (except Audit models)"""
#         app = get_app('bcpp_clinic')
#         for model in get_models(app):
#             if 'Audit' not in model._meta.object_name:
#                 print 'checking for natural key on {0}.'.format(model._meta.object_name)
#                 self.assertTrue('natural_key' in dir(model),
#                                 'natural key not found in {0}'.format(model._meta.object_name))
#
#     def test_p2(self):
#         """Confirms all models have a get_by_natural_key manager method."""
#         app = get_app('bcpp_clinic')
#         for model in get_models(app):
#             if 'Audit' not in model._meta.object_name:
#                 print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
#                 self.assertTrue(
# 'get_by_natural_key' in dir(model.objects),
# 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))
#
#     def test_p3(self):
#         instances = []
#         self.assertEqual(RegisteredSubject.objects.all().count(), 1)
#         registered_subject = RegisteredSubject.objects.all()[0]
#         clinic_eligibility = ClinicEligibilityFactory(registered_subject = registered_subject,
#                                                       dob = registered_subject.dob)
#         self.assertTrue(clinic_eligibility.is_eligible)
#         self.assertEqual(Appointment.objects.all().count(), 1)
#         instances.append(clinic_eligibility)
#
#         print 'INSTANCE: ' + str(instances)
#         for obj in instances:
#             print 'test natural key on {0}'.format(obj._meta.object_name)
#             natural_key = obj.natural_key()
#             get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
#             self.assertEqual(obj.pk, get_obj.pk)
#         # pp = pprint.PrettyPrinter(indent=4)
#         for obj in instances:
#             print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
#             outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj)
#             de = serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
#             for transaction in de:
#                 self.assertEqual(transaction.object.pk, obj.pk)
