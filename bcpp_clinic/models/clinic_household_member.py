from edc_base.encrypted_fields import mask_encrypted

from bhp066.apps.bcpp_household_member.constants import CLINIC_RBD
from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..managers import ClinicHouseholdMemberManager


class ClinicHouseholdMember(HouseholdMember):
    """A proxy model of bcpp_subject.HouseholdMember that bypasses a few features of the
    concrete model."""

    objects = ClinicHouseholdMemberManager()

    def save(self, *args, **kwargs):
        """Saves instance but skips proxy model save."""
        update_fields = kwargs.get('update_fields', [])
        if update_fields == ['member_status', 'enrollment_loss_completed']:
            pass
        else:
            # add to the constraint of first_name, initials, household_structure
            # to accept duplicate first_name, initials, household_structure
            # in the clinic. See unique_together.
            self.eligible_member = self.is_eligible_member
            self.member_status = CLINIC_RBD
            self.absent = False
            self.undecided = False
        super(HouseholdMember, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{0} {1} {2}{3} {4}'.format(
            mask_encrypted(self.first_name),
            self.initials,
            self.age_in_years,
            self.gender,
            'non-BHS')

    class Meta:
        proxy = True
