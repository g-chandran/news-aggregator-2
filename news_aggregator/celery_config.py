import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator.settings')

app = Celery('news_aggregator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = "Asia/Kolkata"

app.conf.beat_schedule = {
    'aggregator': {
        'task': 'start_aggregating',
        'schedule': 60.0 * 2
    }
}
