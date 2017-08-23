import os
from fabric.contrib.files import exists
from edc_fabric.fabfile.virtualenv.tasks import activate_venv
from fabric.api import env, put, cd, run, task

from edc_fabric.fabfile import create_venv
from edc_fabric.fabfile.nginx.tasks import install_nginx
from edc_fabric.fabfile.mysql.tasks import (
    create_database, install_mysql, drop_database)
from edc_fabric.fabfile.gunicorn.tasks import install_gunicorn
from edc_fabric.fabfile.environment.tasks import bootstrap_env,\
    update_fabric_env
from edc_fabric.fabfile.utils import rsync_deployment_root
from edc_fabric.fabfile.python.tasks import install_python3
from edc_fabric.fabfile.utils import launch_webserver
from fabric.utils import abort
from edc_fabric.fabfile.repositories import get_repo_name


def clone_clinic_repo():
    destination = '/Users/django/source/'
    repo_destination = '/Users/django/source/bcpp-clinic/'
    repos = ['edc-dashboard', 'edc-metadata']
    env.project_repo_url = 'https://github.com/botswana-harvard/bcpp-clinic.git'
    gunicorn_file = '/Users/ckgathi/source/bcpp-clinic/fabfile/conf/gunicorn/gunicorn.conf.py'
    if exists(os.path.join(destination, 'bcpp')):
        with(cd(f'{destination}')):
            run('rm -rf bcpp')
    if not exists(destination):
        run(f'mkdir -p {destination}')
    if not exists(repo_destination):
        with(cd(f'{destination}')):
            run('git clone {project_repo_url}'.format(
                project_repo_url=env.project_repo_url))
        with(cd(f'{repo_destination}')):
            run('git checkout master')
            put(os.path.expanduser(gunicorn_file),
                os.path.expanduser(repo_destination))
    else:
        with(cd(f'{repo_destination}')):
            run('git pull')
            run('git checkout master')
            put(os.path.expanduser(gunicorn_file),
                os.path.expanduser(repo_destination))
    for repo in repos:
        if exists(os.path.join(destination, repo)):
            if repo == 'edc-metadata':
                with(cd(os.path(destination))):
                    run(f'rm -rf {repo}')
        else:
            if repo != 'edc-metadata':
                with(cd(f'{destination}')):
                    run(f'git clone https://github.com/botswana-harvard/{repo}.git')
                with cd(destination):
                    run(f'source {activate_venv()} && pip uninstall {repo}', warn_only=True)
                    repo_path = os.path.join(destination, repo)
                    run(f'source {activate_venv()} && pip install -e {repo_path}')


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
                  work_online=True, deployment_root=None, release=None, **kwargs):

    #  Install Mysql,

    #  Create a venv with installed requirements.
    conf_filename = 'bootstrap_client.conf'
    env.deployment_root = deployment_root
    env.etc_dir = '/etc/'
    env.dbname = 'edc'
    env.python_version = 3.6
    env.venv_name = 'bcpp-clinic'
    env.venv_dir = '/Users/django/.venvs/'
    clone_clinic_repo()
    bootstrap_env(
        path=bootstrap_path,
        filename=conf_filename,
        bootstrap_branch=None)
    env.bootstrap_path = bootstrap_path or env.bootstrap_path

    if not release:
        abort('Specify the release')
    if not map_area:
        abort('Specify the map_area')

    env.project_release = release
    env.map_area = map_area

    env.project_repo_name = get_repo_name(env.project_repo_url)
    env.project_repo_root = os.path.join(
        env.deployment_root, env.project_repo_name)
    env.fabric_config_root = os.path.join(env.project_repo_root, 'fabfile')
    env.fabric_config_path = os.path.join(
        env.fabric_config_root, 'conf', env.fabric_conf)

    rsync_deployment_root()

    update_fabric_env()
    if not skip_mysql:
        install_mysql()

    if not skip_python:
        install_python3()
    run('mysql -uroot -pcc3721b drop database edc;', warn_only=True)
    run('mysql -uroot -pcc3721b create database edc character set utf8;',
        warn_only=True)
    create_venv(env.venv_name, env.requirements_file)
    install_nginx(skip_bootstrap=True)
    install_gunicorn(work_online=True)
    launch_webserver()
