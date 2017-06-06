from django.db import models


class ClinicRefusalHistoryManager(models.Manager):

    def get_by_natural_key(self, transaction):
        return self.get(transaction=transaction)
