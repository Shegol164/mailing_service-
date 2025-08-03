from django.core.mail import send_mail
from mailing.models import MailingAttempt
from config import settings


def send_mailing(mailing):
    clients = mailing.clients.all()
    for client in clients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = 'success'
            response = 'Email sent successfully'
        except Exception as e:
            status = 'failure'
            response = str(e)

        MailingAttempt.objects.create(
            mailing=mailing,
            status=status,
            server_response=response
        )

    # Обновляем статус рассылки
    mailing.status = 'started'
    mailing.save()