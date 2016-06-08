from ..models import ClinicRefusal

from edc.dashboard.search.classes import BaseSearchByWord


class RefusalSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = ClinicRefusal
    order_by = '-created'
    template = 'clinicrefusal_include.html'

    def contribute_to_context(self, context):
        context = super(BaseSearchByWord, self).contribute_to_context(context)
        context.update({'refusal_dashboard_url': 'refusal_dashboard_url'}, clinic_refusal_meta=ClinicRefusal._meta,)
        return context
