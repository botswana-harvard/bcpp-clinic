import factory
from datetime import datetime
from edc.subject.visit_tracking.tests.factories import BaseVisitTrackingFactory
from edc.subject.appointment.tests.factories import AppointmentFactory
from ...models import ClinicVisit


class ClinicVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = ClinicVisit

    appointment = factory.SubFactory(AppointmentFactory)
    report_datetime = datetime.today()
    reason = factory.Sequence(lambda n: 'reason{0}'.format(n))
    info_source = factory.Sequence(lambda n: 'info_source{0}'.format(n))
    info_source_other = factory.Sequence(lambda n: 'info_source_other{0}'.format(n))
    subject_identifier = factory.Sequence(lambda n: 'subject_identifier{0}'.format(n))
