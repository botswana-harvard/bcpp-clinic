from django.conf.urls import url

from .admin_site import bcpp_clinic_admin

app_name = 'bcpp_clinic'

urlpatterns = [url(r'^admin/', bcpp_clinic_admin.urls)]
