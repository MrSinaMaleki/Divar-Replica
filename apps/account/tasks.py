from celery import shared_task

@shared_task()
def send_code():
    print("salam")

