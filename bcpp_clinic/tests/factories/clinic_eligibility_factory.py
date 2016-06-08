import factory

from datetime import datetime, date

from ...models import ClinicEligibility


class ClinicEligibilityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ClinicEligibility

    report_datetime = datetime.today()
    identity_type = 'Omang'
    identity = factory.Sequence(lambda n: '88441987{0}'.format(n))
    has_identity = 'Yes'
    citizen = 'Yes'
    literacy = 'Yes'
    first_name = factory.Sequence(lambda n: 'name{0}'.format(n))
    dob = date(date.today().year - 20, 1, 1)
    gender = 'M'
    initials = factory.Sequence(lambda n: 'M{0}'.format(n))
    guardian = 'N/A'
    part_time_resident = (('Yes', 'Yes'), ('No', 'No'), ('DWTA', 'Don\'t want to answer'))[0][0]
    hiv_status = (('POS', 'HIV Positive'), ('NEG', 'HIV Negative'), ('IND', 'Indeterminate'), ('UNK', 'I am not sure'), ('not_answering', 'Don\'t want to answer'))[0][0]
    legal_marriage = 'Yes'
    inability_to_participate = 'N/A'
