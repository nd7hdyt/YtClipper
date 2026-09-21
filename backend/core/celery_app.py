"""
CeleryENconfig
taskqueueconfigENinitialize
"""

import os
from celery import Celery
from celery.schedules import crontab
from pathlib import Path

# settingsENconfigEN
# os.environ.setdefault('CELERY_CONFIG_MODULE', 'backend.core.celery_app')

# createCeleryEN
celery_app = Celery('autoclip')

# configCelery
class CeleryConfig:
    """CeleryconfigEN"""
    
    # taskEN
    task_serializer = 'json'
    accept_content = ['json']
    result_serializer = 'json'
    timezone = 'Asia/Shanghai'
    enable_utc = True
    
    # Redisconfig
    broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # taskconfig
    task_always_eager = os.getenv('CELERY_ALWAYS_EAGER', 'False').lower() == 'true'  # ENexecute
    task_eager_propagates = True
    
    # ENconfig
    worker_prefetch_multiplier = 1
    worker_max_tasks_per_child = 1000
    worker_disable_rate_limits = True
    worker_concurrency = 1  # ENsettingsEN1，ENprocessing
    
    # taskEN
    task_routes = {
        'backend.tasks.processing.*': {'queue': 'processing'},
        'backend.tasks.video.*': {'queue': 'video'},
        'backend.tasks.notification.*': {'queue': 'notification'},
        'backend.tasks.upload.*': {'queue': 'upload'},  # ENuploadtaskEN
        'backend.tasks.import_processing.*': {'queue': 'processing'},  # ENtaskEN
    }
    
    # ENtaskconfig
    beat_schedule = {
        'cleanup-expired-tasks': {
            'task': 'backend.tasks.maintenance.cleanup_expired_tasks',
            'schedule': crontab(hour=2, minute=0),  # EN2EN
        },
        'health-check': {
            'task': 'backend.tasks.maintenance.health_check',
            'schedule': crontab(minute='*/5'),  # EN5EN
        },
    }
    
    # resultconfig
    result_expires = 3600  # 1EN
    task_ignore_result = False
    
    # logconfig
    worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
    worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s'

# ENconfig
celery_app.config_from_object(CeleryConfig)


def _is_desktop_mode() -> bool:
    return os.getenv("AUTOCLIP_DESKTOP_MODE", "").lower() in {"1", "true", "yes"}


class _LocalAsyncResult:
    """EN AsyncResult EN，ENexecuteENreturn。"""

    def __init__(self, task_id: str):
        self.id = task_id
        self.task_id = task_id
        self.state = "PENDING"

    def get(self, *args, **kwargs):
        return None

    def ready(self) -> bool:
        return False


class DesktopAwareTask(celery_app.Task):
    """EN Redis broker，EN core.celery_app EN redis://localhost。

    allEN `task.delay(...)` / `apply_async(...)` ENtask，ENtaskEN
    Redis queue —— EN，EN 0%「initializeEN」。

    EN apply_async EN「ENexecute apply()」：
    EN broker，ENreturn，progressEN。EN。
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
                        f"ENexecutetaskfailed {self.name} ({tid}): {exc}", exc_info=True
                    )

            threading.Thread(target=_run, name=f"task-{self.name}", daemon=True).start()
            return _LocalAsyncResult(tid)

        return super().apply_async(args=args, kwargs=kwargs, task_id=task_id, **options)

    def update_state(self, task_id=None, state=None, meta=None, **kwargs):
        # EN Redis resultEN；taskEN self.update_state() EN ConnectionRefused，
        # ENtaskEN。userENprogressEN simple_progress，EN
        if _is_desktop_mode():
            return None
        return super().update_state(task_id=task_id, state=state, meta=meta, **kwargs)


# ENall @celery_app.task useENexecuteEN
celery_app.Task = DesktopAwareTask

# ENtask
celery_app.autodiscover_tasks([
    'backend.tasks.processing',
    'backend.tasks.video', 
    'backend.tasks.notification',
    'backend.tasks.maintenance',
    'backend.tasks.import_processing'  # ENprocessingtask
])

if __name__ == '__main__':
    celery_app.start()