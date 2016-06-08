from ..search import RefusalSearchByWord

from ..models import ClinicRefusal

from edc.dashboard.section.classes import BaseSectionForDashboardView, site_sections


class SectionRefusalView(BaseSectionForDashboardView):
    section_name = 'refusal'
    section_display_name = 'Clinic Refusals'
    section_display_index = 48
    section_template = 'section_bcpp_refusal.html'
    dashboard_url_name = 'refusal_dashboard_url'
    add_model = ClinicRefusal
    search = {'word': RefusalSearchByWord}
site_sections.register(SectionRefusalView)
