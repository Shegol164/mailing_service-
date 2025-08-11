from django.core.management.base import BaseCommand
from mailing.models import Mailing
from mailing.tasks import send_mailing_task

class Command(BaseCommand):
    help = 'Send scheduled mailings'

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status='created')
        for mailing in mailings:
            send_mailing_task.delay(mailing.id)
            self.stdout.write(f'Sent mailing {mailing.id}')