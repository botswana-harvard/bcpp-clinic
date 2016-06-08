from edc.device.sync.management.commands.consume import Command as BaseCommand

from bhp066.apps.bcpp_clinic_sync.classes import ClinicBcppConsumer


class Command(BaseCommand):

    def get_consumer(self):
        return ClinicBcppConsumer()
