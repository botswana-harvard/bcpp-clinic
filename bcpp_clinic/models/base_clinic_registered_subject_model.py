from datetime import datetime
from django.db import models

from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.device.sync.models import BaseSyncUuidModel
from edc.subject.registration.managers import RegisteredSubjectManager
from edc.subject.registration.models import RegisteredSubject


class BaseClinicRegisteredSubjectModel(BaseSyncUuidModel):

    registration_datetime = models.DateTimeField(
        verbose_name="Registration date/time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),)

    # This is updated by a post save signal
    registered_subject = models.ForeignKey(RegisteredSubject, editable=False, null=True,)

    objects = RegisteredSubjectManager()

    def __unicode__(self):
        return unicode(self.registered_subject)

    def natural_key(self):
        return self.registered_subject.natural_key()

    def get_registered_subject(self):
        return self.registered_subject

    def get_subject_identifier(self):
        """Returns the subject_identifier."""
        return self.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.registration_datetime

    class Meta:
        abstract = True
