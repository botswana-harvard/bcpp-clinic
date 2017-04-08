from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc_base.model.models import HistoricalRecords


from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future, date_not_before_study_start
from edc_sync.model_mixins import SyncModelMixin
from edc_base.model.models import BaseUuidModel
from edc_map.site_mappers import site_mappers

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..managers import BaseClinicHouseholdMemberManager


class ClinicRefusal(SyncModelMixin, BaseUuidModel):
    "A model completed by the user for eligible participants who decide not to participate."""
    household_member = models.OneToOneField(HouseholdMember, null=True)

    refusal_date = models.DateField(
        verbose_name="Date subject refused participation",
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")

    community = models.CharField(max_length=25, editable=False)

    reason = models.CharField(
        verbose_name="We respect your decision to decline. It would help us"
                     " improve the study if you could tell us the main reason"
                     " you do not want to participate in this study?",
        max_length=50,
        choices=(('dont_want', 'I don\'t want to take part'),
                 ('not_sure', 'I am not sure'),
                 ('dont_want_blood_draw', 'I don\'t want to have blood drawn'),
                 ('needles_phobia', 'Fear of needles'),
                 ('privacy', 'I am afraid my information will not be private'),
                 ('illiterate no witness', 'Illiterate does not want a witness'),
                 ('on_haart', 'Already on HAART'),
                 ('knows_status', 'I already know my status'),
                 ('OTHER', 'Other, specify')),
        help_text="")

    reason_other = OtherCharField()

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        null=True,
        blank=True,
        help_text='IMPORTANT: Do not include any names or other personally identifying '
                  'information in this comment')

    history = AuditTrail()

    objects = BaseClinicHouseholdMemberManager()

    def __unicode__(self):
        return "for participant"

    def natural_key(self):
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.householdmember', ]

    def save(self, *args, **kwargs):
        self.community = site_mappers.get_mapper(site_mappers.current_community).map_area
        super(ClinicRefusal, self).save(*args, **kwargs)

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = 'Clinic Refusal'
