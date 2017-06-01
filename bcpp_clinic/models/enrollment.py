from django.db import models
from django.utils import timezone


from ..exceptions import EnrollmentError
from ..managers import EnrollmentManager as BaseEnrollmentManager
from django.db.models.deletion import ProtectedError
from bcpp_subject.models.enrollment import Enrollment,\
    EnrollmentProxyModelManager


class EnrollmentCLinic(Enrollment):

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_clinic.clinic_schedule'
        verbose_name = 'Enrollment Clinic'
        verbose_name_plural = 'Enrollment Clinic'
