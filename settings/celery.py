import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
app = Celery("settings")
app.config_from_object("django.conf:settings", namespace="CELERY")  # CELERY_Name

app.conf.beat_schedule = {
    "check_dates": {
        "task": "training_system/tasks.start",
        "schedule": crontab(minute="0", hour="*/5"),
    }
}

app.autodiscover_tasks()
