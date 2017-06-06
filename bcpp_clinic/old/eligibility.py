from django.apps import apps as django_apps

from edc_constants.constants import YES, NO


class AgeEvaluator:

    def __init__(self, age=None, adult_lower=None,
                 adult_upper=None):
        app_config = django_apps.get_app_config('bcpp_clinic')
        self.age = age
        self.adult_lower = adult_lower or app_config.eligibility_age_adult_lower
        self.adult_upper = adult_upper or app_config.eligibility_age_adult_upper

    @property
    def eligible(self):
        """Returns True if within age range.
        """
        eligible = False
        try:
            if self.adult_lower <= self.age <= self.adult_upper:
                eligible = True
        except TypeError:
            pass
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            if self.age < self.adult_lower:
                reason = f'age<{self.adult_lower}'
            elif self.age > self.adult_upper:
                reason = f'age>{self.adult_upper}'
        return reason


class IdentityEvaluator:

    def __init__(self, has_identity=None, identity=None):
        self.has_identity = has_identity
        self.identity = identity

    @property
    def eligible(self):
        """Returns True if within age range.
        """
        eligible = False
        if self.has_identity == YES and self.identity:
            eligible = True
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            if self.has_identity == NO:
                reason = 'No valid identity.'
        return reason


class CitizenshipEvaluator:

    def __init__(self, citizen=None, legal_marriage=None,
                 marriage_certificate=None):
        self.citizen = citizen
        self.legal_marriage = legal_marriage
        self.marriage_certificate = marriage_certificate

    @property
    def eligible(self):
        """Returns True if citizen or not a citizen and has marriage certicate.
        """
        eligible = False
        if (self.citizen == YES) or (
                self.citizen == NO and self.marriage_certificate == YES and
                    self.legal_marriage == YES):
            eligible = True
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            if self.citizen == NO:
                if self.legal_marriage == YES and self.marriage_certificate == NO:
                    reason = 'Not a citizen, married to a citizen but does not have a marriage certificate.'
                elif self.legal_marriage == NO:
                    reason = 'Not a citizen and not married to a citizen..'
        return reason


class LiteracyEvaluator:

    def __init__(self, literate=None, guardian=None):
        self.literate = literate
        self.guardian = guardian

    @property
    def eligible(self):
        """Returns True if literate or (Not literate and guardian has YES)
        """
        eligible = False
        if self.literate == YES or (
                self.literate == NO and self.guardian == YES):
            eligible = True
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            if self.literate == NO and (not self.guardian or self.guardian == NO):
                reason = 'Illiterate with no literate witness.'
        return reason


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

    @property
    def eligible(self):
        """Returns True if all criteria evaluate True.
        """
        return all(self.criteria.values())

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
