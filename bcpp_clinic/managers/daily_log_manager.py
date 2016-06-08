from django.db import models


class DailyLogManager(models.Manager):

    def get_by_natural_key(self, report_date):
        return self.get(report_date=report_date)
