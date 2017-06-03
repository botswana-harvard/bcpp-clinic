from django import forms

from ..models import ClinicEligibility
from ..utils import get_clinic_member


class ClinicEligibilityForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ClinicEligibilityForm, self).clean()
        options = {}
        try:
            if self.instance.is_consented:
                raise forms.ValidationError('Household member for this checklist has been consented. '
                                            'Eligibility checklist may not be edited')
        except AttributeError:
            pass
        if cleaned_data.get('has_identity') == 'No' and cleaned_data.get('identity'):
            raise forms.ValidationError('You indicated the patient did not provide '
                                        'an identity but identity is provided. Please correct.')
        if cleaned_data.get('has_identity') == 'Yes' and not cleaned_data.get('identity'):
            raise forms.ValidationError('You indicated the patient did has provided '
                                        'an identity but no identity has been provided. Please correct.')
        if cleaned_data.get('identity'):
            if not self.instance:
                self._meta.model.check_for_known_identity(cleaned_data.get('identity'), forms.ValidationError)

        clinic_household_member = cleaned_data.get('clinic_household_member')
        if not clinic_household_member and not self.instance.id:
            options.update(
                first_name=cleaned_data.get('first_name'),
                initials=cleaned_data.get('initials'),
                report_datetime=cleaned_data.get('report_datetime'),
                age_in_years=cleaned_data.get('age_in_years'),
                gender=cleaned_data.get('gender'))
            clinic_household_member = get_clinic_member(**options)
        else:
            raise forms.ValidationError('Clinic Household member is required')
        self.cleaned_data['clinic_household_member'] = clinic_household_member

        self._meta.model.check_for_consent(cleaned_data.get('identity'), forms.ValidationError)

        return cleaned_data

    class Meta:
        model = ClinicEligibility
        fields = '__all__'
