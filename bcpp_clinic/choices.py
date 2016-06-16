from django.utils.translation import ugettext as _

from edc_constants.constants import NOT_APPLICABLE, OTHER

INABILITY_TO_PARTICIPATE_REASON = (
    (NOT_APPLICABLE, _('ABLE to participate')),
    ('Mental Incapacity', _('Mental Incapacity')),
    ('Deaf/Mute', _('Deaf/Mute')),
    ('Too sick', _('Too sick')),
    ('Incarcerated', _('Incarcerated')),
    (OTHER, _('Other, specify.')),
)

VERBALHIVRESULT_CHOICE = (
    ('POS', _('HIV Positive')),
    ('NEG', _('HIV Negative')),
    ('IND', _('Indeterminate')),
    ('UNK', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

COMMUNITIES = (
    ('Bokaa', _('Bokaa')),
    ('Digawana', _('Digawana')),
    ('Gumare', _('Gumare')),
    ('Gweta', _('Gweta')),
    ('Lentsweletau', _('Lentsweletau')),
    ('Lerala', _('Lerala')),
    ('Letlhakeng', _('Letlhakeng')),
    ('Mmandunyane', _('Mmandunyane')),
    ('Mmankgodi', _('Mmankgodi')),
    ('Mmadinare', _('Mmadinare')),
    ('Mmathethe', _('Mmathethe')),
    ('Masunga', _('Masunga')),
    ('Maunatlala', _('Maunatlala')),
    ('Mathangwane', _('Mathangwane')),
    ('Metsimotlhabe', _('Metsimotlhabe')),
    ('Molapowabojang', _('Molapowabojang')),
    ('Nata', _('Nata')),
    ('Nkange', _('Nkange')),
    ('Oodi', _('Oodi')),
    ('Otse', _('Otse')),
    ('Rakops', _('Rakops')),
    ('Ramokgonami', _('Ramokgonami')),
    ('Ranaka', _('Ranaka')),
    ('Sebina', _('Sebina')),
    ('Sefhare', _('Sefhare')),
    ('Sefophe', _('Sefophe')),
    ('Shakawe', _('Shakawe')),
    ('Shoshong', _('Shoshong')),
    ('Tati_Siding', _('Tati_Siding')),
    ('Tsetsebjwe', _('Tsetsebjwe')),
    ('OTHER', _('Other non study community')),
)

WHYNOPARTICIPATE_CHOICE = (
    ('I don\'t have time', _('I don\'t have time')),
    ('I don\'t want to answer the questions', _('I don\'t want to answer the questions')),
    ('I don\'t want to have the blood drawn', _('I don\'t want to have the blood drawn')),
    ('I am afraid my information will not be private', _('I am afraid my information will not be private')),
    ('Fear of needles', _('Fear of needles')),
    ('Illiterate does not want a witness', _('Illiterate does not want a witness')),
    ('I already know I am HIV-positive', _('I already know I am HIV-positive')),
    ('I am afraid of testing', _('I am afraid of testing')),
    ('I don\'t want to take part', _('I don\'t want to take part')),
    ('I haven\'t had a chance to think about it', _('I haven\'t had a chance to think about it')),
    ('Have a newly born baby, not permitted', _('Have a newly born baby, not permitted')),
    ('I am not ready to test', _('I am not ready to test')),
    ('Already on HAART', _('Already on HAART')),
    ('I want to test where i always test', _('I want to test where i always test')),
    ('I already know my partner\'s status, no need to test', _('I already know my partner\'s status, no need to test')),
    ('The appointment was not honoured', _('The appointment was not honoured')),
    ('not_sure', _('I am not sure')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)
