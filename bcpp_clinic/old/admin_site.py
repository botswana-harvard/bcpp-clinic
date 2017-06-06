from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'BCPP Clinic'
    site_header = 'BCPP Clinic'
    index_title = 'BCPP Clinic'
    site_url = '/bcpp_clinic/list/'


bcpp_clinic_admin = AdminSite(name='bcpp_clinic_admin')
