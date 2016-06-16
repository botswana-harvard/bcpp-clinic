from datetime import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from bhp066.apps.bcpp_household_member.constants import NOT_ELIGIBLE, CLINIC_RBD

from .clinic_consent import ClinicConsent
from .clinic_eligibility import ClinicEligibility
from .clinic_enrollment_loss import ClinicEnrollmentLoss
from .clinic_refusal import ClinicRefusal
from .clinic_refusal_history import ClinicRefusalHistory
from registration.models import RegisteredSubject


@receiver(post_save, weak=False, dispatch_uid="clinic_eligibility_on_post_save")
def clinic_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates the household_member instance, if it does not exist, and if not eligible,
    creates a ClinicEnrollmentLoss instance.

    HouseholdMember and RegisteredSubject are always created.
    """
    if not raw:
        if isinstance(instance, ClinicEligibility):
            # use proxy model to avoid save method on household member
            registered_subject = RegisteredSubject.objects.get(pk=instance.registered_subject.pk)
            registered_subject.identity = instance.identity
            registered_subject.identity_type = instance.identity_type
            additional_key = None if instance.identity else instance.additional_key
            registered_subject.additional_key = additional_key
            registered_subject.save()
            if not instance.is_eligible:
                try:
                    clinic_enrollment_loss = ClinicEnrollmentLoss.objects.get(
                        clinic_eligibility=instance)
                    clinic_enrollment_loss.report_datetime = instance.report_datetime
                    clinic_enrollment_loss.reason = '; '.join(instance.loss_reason or [])
                    clinic_enrollment_loss.user_modified = instance.user_modified
                    clinic_enrollment_loss.save()
                except ClinicEnrollmentLoss.DoesNotExist:
                    ClinicEnrollmentLoss.objects.create(
                        clinic_eligibility=instance,
                        report_datetime=instance.report_datetime,
                        reason='; '.join(instance.loss_reason or []),
                        user_created=instance.user_created,
                        user_modified=instance.user_modified)
            else:
                ClinicEnrollmentLoss.objects.filter(clinic_eligibility=instance).delete()


@receiver(post_save, weak=False, dispatch_uid="clinic_consent_on_post_save")
def clinic_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates the is_consented boolean on the eligibility checklist.
    AND Updates or creates an instance of RegisteredSubject on the sender instance"""
    if not raw:
        if isinstance(instance, ClinicConsent):
            clinic_eligibility = ClinicEligibility.objects.get(registered_subject__pk=instance.registered_subject.pk)
            clinic_eligibility.is_consented = True
            clinic_eligibility.consent_datetime = instance.consent_datetime
            clinic_eligibility.save(update_fields=['is_consented', 'consent_datetime'])
            ClinicRefusal.objects.filter(registered_subject__pk=instance.registered_subject.pk).delete()
            try:
                for field_name, value in instance.registered_subject_options.iteritems():
                    setattr(instance.registered_subject, field_name, value)
                instance.registered_subject.subject_identifier = instance.subject_identifier
                instance.registered_subject.save(using=using)
            except AttributeError:
                pass


@receiver(post_save, weak=False, dispatch_uid="clinic_refusal_on_post_save")
def clinic_refusal_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates the is_refused boolean on the eligibility checklist."""
    if not raw:
        if isinstance(instance, ClinicRefusal):
            clinic_eligibility = ClinicEligibility.objects.get(registered_subject__pk=instance.registered_subject.pk)
            clinic_eligibility.is_refused = True
            clinic_eligibility.save(update_fields=['is_refused'])


@receiver(post_delete, weak=False, dispatch_uid="clinic_refusal_on_post_delete")
def clinic_refusal_on_post_delete(sender, instance, using, **kwargs):
    """Delete refusal but first puts a copy into the history model."""
    if isinstance(instance, ClinicRefusal):
        # update the history model
        options = {'household_member': instance.household_member,
                   'refusal_date': instance.refusal_date,
                   'report_datetime': datetime.today(),
                   'survey': instance.household_member.household_structure.survey,
                   'refusal_date': instance.refusal_date,
                   'reason': instance.reason,
                   'reason_other': instance.reason_other}
        ClinicRefusalHistory.objects.using(using).create(**options)
        clinic_eligibility = ClinicEligibility.objects.get(registered_subject__pk=instance.registered_subject.pk)
        clinic_eligibility.is_refused = False
        clinic_eligibility.save(update_fields=['is_refused'])
