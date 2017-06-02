from django.contrib import admin

from ..forms import ClinicConsentForm
from ..models import ClinicConsent
from edc_consent.modeladmin_mixins import ModelAdminConsentMixin
from edc_base.modeladmin_mixins.model_admin_institution_mixin import ModelAdminInstitutionMixin
from edc_base.modeladmin_mixins.model_admin_next_url_redirect_mixin import ModelAdminNextUrlRedirectMixin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from bcpp_clinic.admin_site import bcpp_clinic_admin


@admin.register(ClinicConsent, site=bcpp_clinic_admin)
class ClinicConsentAdmin(ModelAdminConsentMixin, ModelAdminRevisionMixin,
                         ModelAdminInstitutionMixin,
                         ModelAdminNextUrlRedirectMixin, admin.ModelAdmin):

    dashboard_type = 'clinic'
    form = ClinicConsentForm

    list_display = (
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
    fields = (
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

    radio_fields = ({
        'citizen': admin.VERTICAL,
        'legal_marriage': admin.VERTICAL,
        'marriage_certificate': admin.VERTICAL})
