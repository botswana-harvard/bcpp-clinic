import os

from fabric.api import env
from datetime import datetime

from edc_fabric.fabfile.utils import get_hosts, get_device_ids
from edc_fabric.fabfile.environment.tasks import update_env_secrets
from edc_fabric.fabfile.prompts import prompts
from fabric.contrib import django


def load_base_env():
    django.settings_module('bcpp_clinic.settings')

    CONFIG_FILENAME = 'bcpp-clinic.conf'

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ETC_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'etc')
    FABRIC_CONFIG_PATH = os.path.join(
        BASE_DIR, 'fabfile', 'conf', 'fabric.conf')

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    env.log_folder = os.path.expanduser('~/fabric/{}'.format(timestamp))
    if not os.path.exists(env.log_folder):
        os.makedirs(env.log_folder)
    print('log_folder', env.log_folder)
    update_env_secrets(path=ETC_CONFIG_PATH)
    env.hosts, env.passwords = get_hosts(
        path=ETC_CONFIG_PATH, gpg_filename='hosts.conf.gpg')
    env.prompts = prompts

    env.prompts.update({'Enter password: ': env.dbpasswd})