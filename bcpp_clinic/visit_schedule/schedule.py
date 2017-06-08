from edc_visit_schedule.constants import YEARS
from edc_visit_schedule.schedule import Schedule

from .requisitions import requisitions

from ..visit_schedule import crfs


schedule = Schedule(
    name='schedule1',
    title='CLINIC',
    enrollment_model='bcpp_clinic_subject.enrollment',
    disenrollment_model='bcpp_clinic_subject.disenrollment',)

schedule.add_visit(
    code='C1',
    title='Clinic Sibject Survey',
    timepoint=1,
    base_interval=1,
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs)
