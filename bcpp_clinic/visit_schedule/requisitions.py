from edc_visit_schedule.visit import Requisition
from ..labs import rdb_panel, viral_load_panel


requisitions = (
    Requisition(
        show_order=10, model='bcpp_clinic.subjectrequisition',
        panel=rdb_panel, required=False, additional=False),
    Requisition(
        show_order=20, model='bcpp_clinic.subjectrequisition',
        panel=viral_load_panel, required=False, additional=False),
)
