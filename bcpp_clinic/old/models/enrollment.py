from django.db import models
from django.utils import timezone


from django.db.models.deletion import ProtectedError
from member.models.household_member import HouseholdMember
from edc_visit_schedule.model_mixins import EnrollmentModelMixin
from survey.model_mixins import SurveyModelMixin
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_appointment.model_mixins import CreateAppointmentsMixin

from ..exceptions import EnrollmentError
from ..managers import EnrollmentManager as BaseEnrollmentManager


class EnrollmentCLinic(EnrollmentModelMixin, SurveyModelMixin,
                       CreateAppointmentsMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the
    Subject and Anonymous Consents.
    """

    ADMIN_SITE_NAME = 'bcpp_clinic_admin'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    household_member = models.ForeignKey(
        HouseholdMember,
        on_delete=models.PROTECT)

    consent_identifier = models.UUIDField()

    report_datetime = models.DateTimeField(
        default=timezone.now,
        editable=False)

    class Meta:
        visit_schedule_name = 'clinic_visit_schedule.clinic_schedule'
        consent_model = 'bcpp_clinic.clinicconsent'
        verbose_name = 'Enrollment Clinic'
        verbose_name_plural = 'Enrollment Clinic'
