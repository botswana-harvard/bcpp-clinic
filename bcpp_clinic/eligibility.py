from django.apps import apps as django_apps

from edc_constants.constants import YES, NO


class AgeEvaluator:

    def __init__(self, age=None, adult_lower=None,
                 adult_upper=None):
        app_config = django_apps.get_app_config('bcpp_clinic')
        self.age = age
        self.adult_lower = adult_lower or app_config.eligibility_age_adult_lower
        self.adult_upper = adult_upper or app_config.eligibility_age_adult_upper
        self.reason = None
        self.eligible = None
        try:
            if self.adult_lower <= self.age <= self.adult_upper:
                self.eligible = True
        except TypeError:
            pass

        if not self.eligible:
            if self.age < self.adult_lower:
                self.reason = f'age<{self.adult_lower}'
            elif self.age > self.adult_upper:
                self.reason = f'age>{self.adult_upper}'


class IdentityEvaluator:

    def __init__(self, has_identity=None, identity=None):
        self.has_identity = has_identity
        self.identity = identity
        self.eligible = None
        self.reason = None
        if self.has_identity == YES and self.identity:
            self.eligible = True
        if not self.eligible and self.has_identity == NO:
            self.reason = 'No valid identity.'


class CitizenshipEvaluator:

    def __init__(self, citizen=None, legal_marriage=None,
                 marriage_certificate=None):
        self.citizen = citizen
        self.legal_marriage = legal_marriage
        self.marriage_certificate = marriage_certificate
        self.eligible = None
        self.reason = None
        if (self.citizen == YES) or (
                self.citizen == NO and self.marriage_certificate == YES and
                self.legal_marriage == YES):
            self.eligible = True

        if not self.eligible and self.citizen == NO:
                if self.legal_marriage == YES and self.marriage_certificate == NO:
                    self.reason = 'Not a citizen, married to a citizen but does not have a marriage certificate.'
                elif self.legal_marriage == NO:
                    self.reason = 'Not a citizen and not married to a citizen..'


class LiteracyEvaluator:

    def __init__(self, literate=None, guardian=None):
        self.literate = literate
        self.guardian = guardian
        self.eligible = None
        self.reason = None
        if self.literate == YES or (
                self.literate == NO and self.guardian == YES):
            self.eligible = True

        if not self.eligible:
            if self.literate == NO and (not self.guardian or self.guardian == NO):
                self.reason = 'Illiterate with no literate witness.'


class Eligibility:

    def __init__(self, age=None, literate=None, guardian=None, legal_marriage=None,
                 marriage_certificate=None, citizen=None, has_identity=None,
                 identity=None):

        self.age_evaluator = AgeEvaluator(age=age)

        self.citizenship = CitizenshipEvaluator(
            citizen=citizen, legal_marriage=legal_marriage,
            marriage_certificate=marriage_certificate)
        self.identity_evaluator = IdentityEvaluator(
            has_identity=has_identity, identity=identity)
        self.literacy_evaluator = LiteracyEvaluator(
            literate=literate, guardian=guardian)
        self.criteria = dict(
            age=self.age_evaluator.eligible,
            citizen=self.citizenship.eligible,
            has_identity=self.identity_evaluator.eligible,
            literate=self.literacy_evaluator.eligible)
        self.eligible = all(self.criteria.values())

    @property
    def reasons(self):
        """Returns a list of reason not eligible.
        """
        reasons = [k for k, v in self.criteria.items() if not v]
        if self.citizenship.reason:
            reasons.pop(reasons.index('citizen'))
            reasons.append(self.citizenship.reason)
        if self.identity_evaluator.reason:
            reasons.pop(reasons.index('has_identity'))
            reasons.append(self.identity_evaluator.reason)
        if self.literacy_evaluator.reason:
            reasons.pop(reasons.index('literate'))
            reasons.append(self.literacy_evaluator.reason)
        if self.age_evaluator.reason:
            reasons.pop(reasons.index('age'))
            reasons.append(self.age_evaluator.reason)
        return reasons
