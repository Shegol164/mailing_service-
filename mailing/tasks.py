from celery import shared_task
from django.utils import timezone
from mailing.models import Mailing
from mailing.services import send_mailing


@shared_task
def check_mailings():
    now = timezone.now()
    mailings = Mailing.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        status__in=['created', 'started']
    )

    for mailing in mailings:
        send_mailing.delay(mailing.id)