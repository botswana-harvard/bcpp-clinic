from edc_visit_schedule.visit import Crf

_crfs_clinic = (
    Crf(show_order=10, model='bcpp_clinic.questionnaire', required=True),
    Crf(show_order=20, model='bcpp_clinic.viralloadtracking', required=True),
)
