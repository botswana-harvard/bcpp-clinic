from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from edc_constants.constants import NO, YES

from ..exceptions import CLinicEligibilityValidationError
from .clinic_eligibility import ClinicEligibility
from .clinic_enrollment_loss import ClinicEnrollmentLoss
from .clinic_consent import ClinicConsent


@receiver(post_save, weak=False, dispatch_uid="clinic_eligibility_on_post_save")
def clinic_eligibility_on_post_save(
        sender, instance, raw, created, using, **kwargs):
    """Creates or deletes ClinicEnrollmentLoss instance.
    """
    if not raw:
        if not instance.is_eligible:
            try:
                enrollment_loss = ClinicEnrollmentLoss.objects.get(
                    clinic_household_member=instance.clinic_household_member)
                enrollment_loss.report_datetime = instance.report_datetime
                enrollment_loss.reason = instance.loss_reason
                enrollment_loss.save()
            except ClinicEnrollmentLoss.DoesNotExist:
                enrollment_loss = ClinicEnrollmentLoss(
                    clinic_household_member=instance.clinic_household_member,
                    report_datetime=instance.report_datetime,
                    reason=instance.loss_reason)
                enrollment_loss.save()
            instance.clinic_household_member.eligible_subject = False
        else:
            enrollment_loss = ClinicEnrollmentLoss.objects.filter(
                clinic_household_member=instance.clinic_household_member).delete()
            instance.clinic_household_member.eligible_subject = True
        instance.clinic_household_member.enrollment_checklist_completed = True

        if created:
            instance.clinic_household_member.visit_attempts += 1
        instance.clinic_household_member.non_citizen = instance.non_citizen
        instance.clinic_household_member.citizen = instance.citizen == YES
        instance.clinic_household_member.spouse_of_citizen = (
            instance.citizen == NO
            and instance.legal_marriage == YES
            and instance.marriage_certificate == YES)
        instance.clinic_household_member.save()


@receiver(post_save, weak=False, dispatch_uid="clinic_consent_on_post_save")
def clinic_consent_on_post_save(
        sender, instance, raw, created, using, **kwargs):
    """Updates the is_consented boolean on the clinic eligibility.
    """
    if not raw:
        try:
            clinic_eligibility = ClinicEligibility.objects.get(
                clinic_household_member=instance.clinic_household_member)
        except ClinicEligibility.DoesNotExist:
            raise CLinicEligibilityValidationError(
                "Clinic Eligibility required.")
        else:
            clinic_eligibility.is_consented = True
            clinic_eligibility.consent_datetime = instance.consent_datetime
            clinic_eligibility.save(
                update_fields=['is_consented', 'consent_datetime'])


@receiver(post_save, weak=False, dispatch_uid='consent_on_post_save')
def consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if issubclass(sender, (ClinicConsent)):
            # update clinic household member field attrs
            instance.clinic_household_member.absent = False
            instance.clinic_household_member.undecided = False
            instance.clinic_household_member.refused = False
            instance.clinic_household_member.subject_identifier = instance.subject_identifier
            instance.clinic_household_member.save()
            instance.clinic_household_member.household_structure.enrolled = True
            instance.clinic_household_member.household_structure.save()
