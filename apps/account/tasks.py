from celery import shared_task
from services.mail import MailProvider

@shared_task()
def send_email(subject, recipient, template, context):
    try:
        mail_provider = MailProvider(subject, recipient, template, context)
        mail_provider.send()
    except Exception as e:
        print(f"Failed to send email to {recipient}: {str(e)}")

