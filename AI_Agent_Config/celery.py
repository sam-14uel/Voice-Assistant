import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AI_Agent_Config.settings")
app = Celery("AI_Agent_Config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()