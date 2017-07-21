from os.path import exists

from fabric.api import env, put, sudo, cd, run, warn, prefix, lcd, task

from edc_fabric.fabfile import create_venv
from edc_fabric.fabfile.nginx.tasks import install_nginx
from edc_fabric.fabfile.mysql.tasks import (
    create_database, install_mysql, drop_database)
from edc_fabric.fabfile.gunicorn.tasks import install_gunicorn
from edc_fabric.fabfile.environment.tasks import bootstrap_env,\
    update_fabric_env
from edc_fabric.fabfile.python.tasks import install_python3


def clone_clinic_repo():
    destination = '/Users/django/source/'
    repo_destination = '/Users/django/source/bcpp-clinic/'
    if not exists(destination):
        run(f'mkdir -p {destination}')
#     if not exists(repo_destination):
#         with(cd(f'{destination}')):
#             run('git clone {project_repo_url}'.format(
#                 project_repo_url=env.project_repo_url))
#     else:
    with(cd(f'{repo_destination}')):
        run('git pull')


@task
def deploy(**kwargs):
    """For example:

    Copy ssh keys:

        fab -P -R mmankgodi deploy.ssh_copy_id:bootstrap_path=/Users/ckgathi/source/bcpp-clinic/fabfile/conf,bootstrap_branch=develop --user=django

    Deploy:[

        fab -H bcpp038 deploy.deploy_client:bootstrap_path=/Users/ckgathi/source/bcpp-clinic/fabfile/conf/,map_area=mmankgodi --user=django

    - OR -

        fab -P -R mmankgodi deploy.deploy_client:bootstrap_path=/Users/ckgathi/source/bcpp-clinic/fabfile/conf/,map_area=mmankgodi --user=django
    """

    conf_filename = 'bootstrap_client.conf'
    deploy_client(conf_filename=conf_filename, **kwargs)


def deploy_client(conf_filename=None, bootstrap_path=None, map_area=None, user=None,
                  bootstrap_branch=None, skip_mysql=None, skip_python=None,
                  work_online=True, deployment_root=None, **kwargs):

    #  Install Mysql,

    #  Create a venv with installed requirements.
    conf_filename = 'bootstrap_client.conf'
    env.deployment_root = deployment_root
    env.etc_dir = '/etc/'
    env.dbname = 'edc_clinic'
    env.python_version = 3.6
    env.venv_name = 'bcpp-clinic'
    env.venv_dir = '/Users/django/.venvs/'

    bootstrap_env(
        path=bootstrap_path,
        filename=conf_filename,
        bootstrap_branch=None)
    env.bootstrap_path = bootstrap_path or env.bootstrap_path
    update_fabric_env()
    if not skip_mysql:
        install_mysql()

    if not skip_python:
        install_python3()
    drop_database(
        dbname='edc_clinic', dbuser='root', dbpasswd='cc3721b')
    create_database(
        dbname='edc_clinic', dbuser='root', dbpasswd='cc3721b')
#     clone_clinic_repo()
    create_venv(env.venv_name, env.requirements_file, work_online=True)
    install_nginx(**kwargs)
    install_gunicorn(work_online=True)
