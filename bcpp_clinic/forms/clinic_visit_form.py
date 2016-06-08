from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import ClinicVisit


class ClinicVisitForm (BaseModelForm):

    class Meta:
        model = ClinicVisit
