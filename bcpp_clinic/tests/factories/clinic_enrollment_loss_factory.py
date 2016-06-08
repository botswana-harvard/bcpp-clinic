import factory
from datetime import datetime

from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from ...models import ClinicEnrollmentLoss


class ClinicEnrollmentLossFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ClinicEnrollmentLoss

    registration_datetime = datetime.today()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    first_name = factory.Sequence(lambda n: 'name{0}'.format(n))
    reason = factory.Sequence(lambda n: 'reason{0}'.format(n))
