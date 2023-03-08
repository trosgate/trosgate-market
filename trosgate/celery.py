from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# from django_celery_beat.models import PeriodicTask
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trosgate.settings')

# app = Celery('trosgate', broker_url = 'redis://127.0.0.1:6379') #or broker_url in place of broker
app = Celery('trosgate') 
# ### if CELERY_TIMEZONE is specified in settings.py other than UTC, then activate below utc to False ###
app.conf.enable_utc = True
# app.conf.update(timezone = 'Africa/Accra')

app.config_from_object ('django.conf:settings', namespace='CELERY') #This will tell django not to pickle on windows OS

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# ### Celery beat settings ### only required if you want to schedule mail at some specific time

app.conf.beat_schedule ={
    # Will execute everyday 1 minutes interval
    'sync-domains':{
        'task':'sync_domains',
        'schedule': crontab(minute='*/1')
    },
    # # Will execute at 7pm-7pm everyday of the week at an interval of 10min
    # 'ongoing-tickets-paused-between-7pm-to-11pm':{
    #     'task':'ongoing_ticket_paused_by_end_of_working_hours',
    #     'schedule': crontab(minute='*/30', hour='19-23', day_of_week='sun-sat')
    # },

}


# @app.task(bind = True)
# def debug_task(self):
#     print(f'request: {self.request!r}')