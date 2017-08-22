import os

bind = "127.0.0.1:9000"  # Don't use port 80 because nginx occupied it already.
errorlog = os.path.expanduser('~/log/gunicorn-error.log')  # M$
accesslog = os.path.expanduser('~/log/gunicorn-access.log')
loglevel = 'debug'
workers = 1  # the number of recommended workers is '2 * number of CPUs + 1'
timeout = 300
