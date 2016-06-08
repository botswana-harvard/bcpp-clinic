import factory

from datetime import datetime

from edc.testing.tests.factories.test_consent_factory import BaseConsentFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from ...models import ClinicConsent


class ClinicConsentFactory(BaseConsentFactory):
    FACTORY_FOR = ClinicConsent

    # subject_identifier = None
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    consent_datetime = datetime.today()
    may_store_samples = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    is_literate = (('Yes', 'Yes'), ('No', 'No'))[0][0]
#     consent_version_on_entry = 1
#     consent_version_recent = 1
    is_verified = True
    identity = factory.Sequence(lambda n: '31791851{0}'.format(n))
    identity_type = (('OMANG', 'Omang'),
                     ('DRIVERS', "Driver's License"),
                     ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'),
                     ('OTHER', 'Other'))[0][0]
    confirm_identity = identity
