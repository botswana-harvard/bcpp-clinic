from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class ClinicSubjectLocatorIsReferredListFilter(SimpleListFilter):

    title = _('referred')

    parameter_name = 'referred'

    def lookups(self, request, model_admin):
        return ((True, 'Yes'), (False, 'No'), )
