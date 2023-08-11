from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

logger = get_task_logger(__name__)


@shared_task
def send_email(email):
    logger.info("Sent email")
    send_mail('Contact from',
              'Thanks for signing in',
              'settings.EMAIL_HOST_USER',
              [email],
              fail_silently=False,
              )
