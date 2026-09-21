"""
Celerytranslateduseconfig
Task QueueconfigAndtranslated
"""

import os
from celery import Celery
from celery.schedules import crontab
from pathlib import Path

# settingsdefaultconfigtranslated
# os.environ.setdefault('CELERY_CONFIG_MODULE', 'backend.core.celery_app')

# createCelerytranslateduse
celery_app = Celery('autoclip')

# configCelery
class CeleryConfig:
    """Celeryconfigtranslated"""
    
    # tasktranslatedformat
    task_serializer = 'json'
    accept_content = ['json']
    result_serializer = 'json'
    timezone = 'Asia/Shanghai'
    enable_utc = True
    
    # Redisconfig
    broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # taskconfig
    task_always_eager = os.getenv('CELERY_ALWAYS_EAGER', 'False').lower() == 'true'  # translated
    task_eager_propagates = True
    
    # translatedprocessconfig
    worker_prefetch_multiplier = 1
    worker_max_tasks_per_child = 1000
    worker_disable_rate_limits = True
    worker_concurrency = 1  # translatedsettingstranslated1，translatedprocess
    
    # tasktranslated
    task_routes = {
        'backend.tasks.processing.*': {'queue': 'processing'},
        'backend.tasks.video.*': {'queue': 'video'},
        'backend.tasks.notification.*': {'queue': 'notification'},
        'backend.tasks.upload.*': {'queue': 'upload'},  # adduploadtasktranslated
        'backend.tasks.import_processing.*': {'queue': 'processing'},  # importtasktranslated
    }
    
    # translatedtaskconfig
    beat_schedule = {
        'cleanup-expired-tasks': {
            'task': 'backend.tasks.maintenance.cleanup_expired_tasks',
            'schedule': crontab(hour=2, minute=0),  # pertranslated2translated
        },
        'health-check': {
            'task': 'backend.tasks.maintenance.health_check',
            'schedule': crontab(minute='*/5'),  # per5minutes
        },
    }
    
    # translatedconfig
    result_expires = 3600  # 1translated
    task_ignore_result = False
    
    # logsconfig
    worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
    worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s'

# translateduseconfig
celery_app.config_from_object(CeleryConfig)


def _is_desktop_mode() -> bool:
    return os.getenv("AUTOCLIP_DESKTOP_MODE", "").lower() in {"1", "true", "yes"}


class _LocalAsyncResult:
    """translated AsyncResult translated，translatedlocaltranslatedreturn。"""

    def __init__(self, task_id: str):
        self.id = task_id
        self.task_id = task_id
        self.state = "PtranslatedDING"

    def get(self, *args, **kwargs):
        return None

    def ready(self) -> bool:
        return False


class DesktopAwareTask(celery_app.Task):
    """translatedinstallPackagetranslated Redis broker，translated core.celery_app translated redis://localhost。

    translateduse `task.delay(...)` / `apply_async(...)` translatedtask，defaulttranslated tasktranslated
    Redis translated —— translated，translatedIstranslatedin 0%「translated」。

    thistranslatedintranslated  apply_async translated「intranslated apply()」：
    translateddependenciestranslated broker，translatedreturn，progresstranslatedfrontendtranslated。translated。
    """

    def apply_async(self, args=None, kwargs=None, task_id=None, **options):
        if _is_desktop_mode():
            import threading
            import uuid

            tid = task_id or str(uuid.uuid4())
            call_args = list(args) if args else []
            call_kwargs = dict(kwargs) if kwargs else {}

            def _run():
                try:
                    self.apply(args=call_args, kwargs=call_kwargs, task_id=tid)
                except Exception as exc:  # noqa: BLE001
                    import logging
                    logging.getLogger(__name__).error(
                        f"translatedlocaltranslatedtaskfailed {self.name} ({tid}): {exc}", exc_info=True
                    )

            threading.Thread(target=_run, name=f"task-{self.name}", daemon=True).start()
            return _LocalAsyncResult(tid)

        return super().apply_async(args=args, kwargs=kwargs, task_id=task_id, **options)

    def update_state(self, task_id=None, state=None, meta=None, **kwargs):
        # translated Redis translatedbackend；tasktranslated's self.update_state() translated ConnectionRefused，
        #  translatedimporttasktranslated。usercantranslatedprogresstranslated simple_progress，thistranslatedcan
        if _is_desktop_mode():
            return None
        return super().update_state(task_id=task_id, state=state, meta=meta, **kwargs)


# translated @celery_app.task usetranslated'slocaltranslated
celery_app.Task = DesktopAwareTask

# translatedtask
celery_app.autodiscover_tasks([
    'backend.tasks.processing',
    'backend.tasks.video', 
    'backend.tasks.notification',
    'backend.tasks.maintenance',
    'backend.tasks.import_processing'  # addimportprocesstask
])

if __name__ == '__main__':
    celery_app.start()