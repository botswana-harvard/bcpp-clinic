from django.contrib import admin

from edc_consent.admin import BaseConsentModelAdmin

from ..forms import ClinicConsentForm
from ..models import ClinicConsent


class ClinicConsentAdmin(BaseConsentModelAdmin):

    dashboard_type = 'clinic'
    form = ClinicConsentForm

    def __init__(self, *args, **kwargs):
        super(ClinicConsentAdmin, self).__init__(*args, **kwargs)
        self.list_filter = list(self.list_filter)
        self.list_filter.append('community')
        self.list_filter = tuple(self.list_filter)

        self.search_fields = list(self.search_fields)
        self.search_fields.append('first_name')
        self.search_fields.append('htc_identifier')
        self.search_fields.append('lab_identifier')
        self.search_fields.append('pims_identifier')
        self.search_fields = tuple(self.search_fields)
#         self.list_display.insert(1, 'htc_identifier')
#         self.list_display.insert(2, 'lab_identifier')
#         self.list_display.insert(3, 'pims_identifier')
        self.list_display = (
            'subject_identifier',
            'htc_identifier',
            'lab_identifier',
            'pims_identifier',
            'is_verified',
            'is_verified_datetime',
            'first_name',
            'initials',
            'gender',
            'dob',
            'consent_datetime',
            'created',
            'modified',
            'user_created',
            'user_modified'
        )
        self.fields = (
            'subject_identifier',
            'first_name',
            'last_name',
            'initials',
            'language',
            'is_literate',
            'witness_name',
            'consent_datetime',
            'study_site',
            'gender',
            'dob',
            'guardian_name',
            'is_dob_estimated',
            'citizen',
            'legal_marriage',
            'marriage_certificate',
            'marriage_certificate_no',
            'identity',
            'identity_type',
            'confirm_identity',
            'may_store_samples',
            'comment',
            'consent_reviewed',
            'study_questions',
            'assessment_score',
            'consent_copy',
            'lab_identifier',
            'htc_identifier',
            'pims_identifier')
        self.radio_fields.update({'citizen': admin.VERTICAL,
                                  'legal_marriage': admin.VERTICAL,
                                  'marriage_certificate': admin.VERTICAL})

admin.site.register(ClinicConsent, ClinicConsentAdmin)
