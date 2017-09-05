#!/bin/bash
source /Users/django/.venvs/bcpp-clinic/bin/activate && \
cd /Users/django/source/bcpp-clinic && \
python manage.py export_transactions --user=django@communityserver --target_path=/Users/django/media/transactions/incoming
