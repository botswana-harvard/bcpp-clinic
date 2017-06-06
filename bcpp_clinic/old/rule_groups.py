from edc.subject.rule_groups.classes import RuleGroup, site_rule_groups, Logic, ScheduledDataRule, RequisitionRule

from .models import ClinicVisit, ViralLoadTracking, Questionnaire


class InitiationRequisitionRuleGroup(RuleGroup):

    initiation = RequisitionRule(
        logic=Logic(
            predicate=(('registration_type', 'equals', 'initiation'), ('registration_type', 'equals', 'OTHER', 'or')),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'clinicrequisition')],
        target_requisition_panels=['Clinic Viral Load'],)

    class Meta:
        app_label = 'bcpp_clinic'
        source_fk = (ClinicVisit, 'clinic_visit')
        source_model = Questionnaire
site_rule_groups.register(InitiationRequisitionRuleGroup)


class MasaRuleGroup(RuleGroup):

    is_drawn = ScheduledDataRule(
        logic=Logic(
            predicate=(('registration_type', 'equals', 'masa_vl_scheduled')),
            consequence='new',
            alternative='not_required'),
        target_model=['viralloadtracking'])

    class Meta:
        app_label = 'bcpp_clinic'
        source_fk = (ClinicVisit, 'clinic_visit')
        source_model = Questionnaire
site_rule_groups.register(MasaRuleGroup)


class ViralLoadTrackingRuleGroup(RuleGroup):

    is_drawn = ScheduledDataRule(
        logic=Logic(
            predicate=('is_drawn', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['clinicvlresult'])

    class Meta:
        app_label = 'bcpp_clinic'
        source_fk = (ClinicVisit, 'clinic_visit')
        source_model = ViralLoadTracking
site_rule_groups.register(ViralLoadTrackingRuleGroup)


class ViralLoadTrackingRequisitionRuleGroup(RuleGroup):

    initiation = RequisitionRule(
        logic=Logic(
            predicate=('is_drawn', 'equals', 'No'),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'clinicrequisition')],
        target_requisition_panels=['Clinic Viral Load'],)

    class Meta:
        app_label = 'bcpp_clinic'
        source_fk = (ClinicVisit, 'clinic_visit')
        source_model = ViralLoadTracking
site_rule_groups.register(ViralLoadTrackingRequisitionRuleGroup)
