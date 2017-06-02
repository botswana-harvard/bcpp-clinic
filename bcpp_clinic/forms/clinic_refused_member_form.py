from django import forms

from ..models import ClinicRefusedMember


class ClinicRefusedMemberForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ClinicRefusedMemberForm, self).clean()

        return cleaned_data

    class Meta:
        model = ClinicRefusedMember
        fields = '__all__'
