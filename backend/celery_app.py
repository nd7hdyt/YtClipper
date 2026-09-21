"""
ENCeleryENconfig
ENserviceENconfig
"""

import os

IS_DESKTOP = os.getenv("AUTOCLIP_DESKTOP_MODE") == "1"

if IS_DESKTOP:
    # ENusefilesystem broker / sqlite backend EN Celery
    from .desktop_celery import celery_app  # noqa: F401
else:
    # serviceEN/EN：Redis ENconfigEN broker/backend
    from celery import Celery

    broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

    celery_app = Celery(__name__, broker=broker_url, backend=backend_url)
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Shanghai',
        enable_utc=True,
        task_always_eager=False,  # serviceENexecute
        task_eager_propagates=True,
        result_expires=3600,
        task_ignore_result=False,
        task_routes={
            'backend.tasks.processing.*': {'queue': 'processing'},
            'backend.tasks.video.*': {'queue': 'video'},
            'backend.tasks.notification.*': {'queue': 'notification'},
            'backend.tasks.maintenance.*': {'queue': 'maintenance'},
            'backend.tasks.upload.*': {'queue': 'upload'},
        },
    )

# ENtask
celery_app.autodiscover_tasks([
    'backend.tasks.processing',
    'backend.tasks.video', 
    'backend.tasks.notification',
    'backend.tasks.maintenance',
    'backend.tasks.upload'
])

if __name__ == '__main__':
    celery_app.start()

