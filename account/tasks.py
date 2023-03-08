from django.core.management import call_command
from celery import shared_task


@shared_task()
def update_my_domains():
    call_command("update_domains")








