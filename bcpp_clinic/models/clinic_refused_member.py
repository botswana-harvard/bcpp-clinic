from member.models import RefusedMember


class ClinicRefusedMember(RefusedMember):
    "A model completed by the user for eligible participants who decide not to participate."""

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = 'Clinic Refused Member'
        proxy = True
