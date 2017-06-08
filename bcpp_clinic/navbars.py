from edc_base.navbar_item import NavbarItem

navbars = {}
navbar_items = []
config = [
    ('clinic_subject', 'subjects', 'fa-user-circle-o', 'listboard_url_name'),
    ('clinic_screening', 'Screening',
     'fa-user-circle-o', 'listboard_url_name'),
    ('edc_lab', None, 'fa-flask', 'home_url_name')
]
for app_config_name, label, fa_icon, app_config_attr in config:
    navbar_item = NavbarItem(
        app_config_name=app_config_name,
        label=label,
        fa_icon=fa_icon,
        app_config_attr=app_config_attr)
    navbar_items.append(navbar_item)
navbars.update(default=navbar_items)
