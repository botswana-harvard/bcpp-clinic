from edc_constants.constants import NOT_APPLICABLE

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
