import sys

if 'fab' in sys.argv[0]:
    from edc_fabric import fabfile as common
    from .deploy import deploy_client, deploy
    from .local_base_env import load_base_env

    load_base_env()
