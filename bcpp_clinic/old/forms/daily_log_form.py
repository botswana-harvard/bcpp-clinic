from django import forms

from ..models import DailyLog


class DailyLogForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(DailyLogForm, self).clean()

        return cleaned_data

    class Meta:
        model = DailyLog
        fields = '__all__'
