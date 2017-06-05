from django.utils.translation import ugettext_lazy as _
from edc_constants.constants import NOT_APPLICABLE, POS, NEG, IND, UNK, OTHER

from .constants import BLOCK_PARTICIPATION, CONTINUE_PARTICIPATION

BLOCK_CONTINUE = (
    (BLOCK_PARTICIPATION, 'Yes (Do not allow further participation)'),
    (CONTINUE_PARTICIPATION, 'No (May continue and participate)'),
    (NOT_APPLICABLE, 'Not applicable'),
)

REGISTRATION_TYPES = (
    ('initiation', 'Initiation Visit'),
    ('masa_vl_scheduled', 'MASA Scheduled Viral Load Visit'),
    ('OTHER', 'Other NON-Viral Load Visit')
)

VERBALHIVRESULT_CHOICE = (
    (POS, _('HIV Positive')),
    (NEG, _('HIV Negative')),
    (IND, _('Indeterminate')),
    (UNK, _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

VISIT_UNSCHEDULED_REASON = (
    ('Routine oncology',
     _('Routine oncology clinic visit (i.e. planned chemo, follow-up)')),
    ('Ill oncology', _('Ill oncology clinic visit')),
    ('Patient called', _('Patient called to come for visit')),
    (OTHER, _('Other, specify:')),
)
