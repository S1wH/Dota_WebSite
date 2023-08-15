from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core import mail

logger = get_task_logger(__name__)


@shared_task
def send_email(email):
    with mail.get_connection() as connection:
        logger.info("Sent email")
        mail.EmailMessage(
            subject='Contact from',
            body='Thanks for signing in',
            from_email='settings.EMAIL_HOST_USER',
            to=[email],
            connection=connection
        ).send()
