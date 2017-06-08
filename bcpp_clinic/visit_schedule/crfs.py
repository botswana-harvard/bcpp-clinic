from edc_visit_schedule.visit import Crf

_crfs = (
    Crf(show_order=10, model='bcpp_clinic_subject.questionnaire', required=True),
    Crf(show_order=20, model='bcpp_clinic_subject.viralloadtracking',
        required=True),
)
