from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin

from ..models import ClinicVisit


class ClinicVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the clinic visit model."""

    visit_model = ClinicVisit
    visit_attr = 'clinic_visit'
    dashboard_type = 'clinic'
    date_heirarchy = 'clinic_visit__report_datetime'
