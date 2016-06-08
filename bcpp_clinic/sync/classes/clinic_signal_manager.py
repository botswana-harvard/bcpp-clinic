from django.db.models import signals

from bhp066.apps.bcpp_clinic.models import clinic_eligibility_on_post_save


class ClinicSignalManager(object):

    def _disconnect_clinic_signals(self):
        """Disconnects signals before saving the serialized object in _to_json."""
        signals.post_save.disconnect(
            clinic_eligibility_on_post_save, weak=False, dispatch_uid="clinic_eligibility_on_post_save")

    def _reconnect_clinic_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
        signals.post_save.connect(
            clinic_eligibility_on_post_save, weak=False, dispatch_uid="clinic_eligibility_on_post_save")
