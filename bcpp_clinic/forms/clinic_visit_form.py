from django import forms

from ..models import ClinicVisit


class ClinicVisitForm (forms.ModelForm):

    class Meta:
        model = ClinicVisit
        fields = '__all__'
