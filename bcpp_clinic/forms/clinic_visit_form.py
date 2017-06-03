from django import forms

from edc_visit_tracking.form_mixins import VisitFormMixin

from ..models import ClinicVisit


class ClinicVisitForm (VisitFormMixin, forms.ModelForm):

    class Meta:
        model = ClinicVisit
        fields = '__all__'
