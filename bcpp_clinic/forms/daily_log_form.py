from ..models import DailyLog
from .modelform_mixin import ClinicModelFormMixin


class DailyLogForm(ClinicModelFormMixin):

    class Meta:
        model = DailyLog
        fields = '__all__'
