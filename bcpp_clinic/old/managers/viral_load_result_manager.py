from django.db import models


class ViralLoadResultManager(models.Manager):

    def get_by_natural_key(self, sample_id):
        return self.get(sample_id=sample_id)
