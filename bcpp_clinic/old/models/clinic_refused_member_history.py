from member.models import RefusedMemberHistory


class ClinicRefusedMemberHistory(RefusedMemberHistory):
    """A system model that tracks the history of deleted refusal instances."""

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Refused Member History'
        verbose_name_plural = 'Clinic Refused Member History'
        proxy = True
