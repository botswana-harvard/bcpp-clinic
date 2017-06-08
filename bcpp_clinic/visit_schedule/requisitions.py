from edc_visit_schedule.visit import Requisition

from ..labs import panel_rbd, panel_vl


requisitions = (
    Requisition(
        show_order=10, model='bcpp_clinic_subject.subjectrequisition',
        panel=panel_rbd, required=False, additional=False),
    Requisition(
        show_order=20, model='bcpp_clinic_subject.subjectrequisition',
        panel=panel_vl, required=False, additional=False),
)
