from ..models import DailyLog
from .model_form_mixin import CLinicModelFormMixin


class DailyLogForm(CLinicModelFormMixin):

    def clean(self):
        cleaned_data = super(DailyLogForm, self).clean()

        return cleaned_data

    class Meta:
        model = DailyLog
        fields = '__all__'
