from edc_visit_schedule.constants import YEARS
from edc_visit_schedule.schedule import Schedule

from .requisitions import requisitions
from bcpp_clinic.visit_schedule import crfs_clinic


clinic_schedule = Schedule(name='clinic_schedule', title='CLINIC')

clinic_schedule.add_visit(
    code='C1',
    title='Clinic Survey',
    timepoint=1,
    base_interval=1,
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_clinic)
