# from __future__ import absolute_import, unicode_literals
# import os

# from celery import Celery
# from celery.schedules import crontab
# # from django_celery_beat.models import PeriodicTask
# from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trosgate.settings')

# app = Celery('trosgate', broker_url = 'redis://127.0.0.1:6379')

# ### if CELERY_TIMEZONE is specified in settings.py,  then activate below utc to True ###
# app.conf.enable_utc = False
# app.conf.update(timezone = 'Africa/Accra')

# app.config_from_object (settings, namespace='CELERY')

# ### Celery beat settings ### only required if you want to schedule mail at some specific time
# app.conf.beat_schedule ={
#     'schedule_mail_in_future':{
#         'task':'teams.tasks.email_all_users',
#         'schedule': crontab(hour=18, minute=27),
#         # 'args': (enter argument)
#     }
# }

# app.autodiscover_tasks()

# @app.task(bind = True)
# def debug_task(self):
#     print(f'request: {self.request!r}')









