from __future__ import absolute_import, unicode_literals
import os

from datetime import timedelta
from celery import Celery
from django.conf import settings
from ear_info.task import job

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ear_control_site.settings')

app = Celery('ear_control_site')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.update(
	CELERYBEAT_SCHEDULE={
		'per5minute': {
			'task': 'tasks.crawing_job',
			'schedule': timedelta(seconds=15),
			'args': ('C:/Users/06101181/djangoWorkspace/ear_control_site/phantomjs.exe','C:/Users/06101181/djangoWorkspace/ear_control_site/db.sqlite3')
		}
	}
)

@app.task(name='tasks.crawing_job')
def crawing_job(phantomjs_path='C:/Users/06101181/djangoWorkspace/ear_control_site/phantomjs.exe', db_path = 'C:/Users/06101181/djangoWorkspace/ear_control_site/db.sqlite3'):
	job(phantomjs_path, db_path)
	return ' crawling_job run success. '
