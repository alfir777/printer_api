import sys

from django.apps import AppConfig
from django_rq import get_scheduler


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Контроль печати чеков'

    def ready(self):
        from core.tasks import streams_tasks

        if "rqscheduler" not in sys.argv:
            return

        scheduler = get_scheduler('default', interval=10)

        for job in scheduler.get_jobs():
            job.delete()

        streams_tasks(scheduler)
