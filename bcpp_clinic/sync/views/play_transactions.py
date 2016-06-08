import socket
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from ..classes import ClinicBcppConsumer


@login_required
def play_transactions(request, **kwargs):
    """ Play all the incoming transactions pending on the server
    """
    consumer = ClinicBcppConsumer()
    # TODO: this should not allow errors to pass!!
    try:
        consumer.consume()
    except:
        pass
    message = consumer.get_consume_feedback()
    messages.add_message(request, messages.INFO, message)
    if 'EMAIL_AFTER_CONSUME' in dir(settings) and settings.EMAIL_AFTER_CONSUME:
        if not (settings.EMAIL_HOST or settings.EMAIL_PORT or settings.EMAIL_HOST_USER or settings.EMAIL_HOST_PASSWORD):
            raise ImproperlyConfigured(
                "Ensure that EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD are set in "
                "the email_settings file")
        send_mail(
            'Consuming status of BCPP incoming transactions;-' + str(socket.gethostname()), message,
            settings.EMAIL_HOST_USER + '@bhp.org.bw', ['django@bhp.org.bw'], fail_silently=False)

    url = reverse('bccp_sync_url')
    return redirect(url)
