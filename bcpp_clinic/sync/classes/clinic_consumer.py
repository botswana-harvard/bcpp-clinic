from edc.device.sync.classes import Consumer

from .clinic_signal_manager import ClinicSignalManager


class ClinicBcppConsumer(Consumer, ClinicSignalManager):

    def disconnect_signals(self):
        """Disconnects signals before saving the serialized object in _to_json."""
        self._disconnect_clinic_signals()

    def reconnect_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
        self._reconnect_clinic_signals()
