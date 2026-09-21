"""
ENCeleryENconfig
EN，ENtaskEN
"""

import os
from celery import Celery

# createCeleryEN
celery_app = Celery('autoclip')

# ENconfig
celery_app.conf.update(
    # EN
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Redisconfig
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    
    # EN
    timezone='Asia/Shanghai',
    enable_utc=True,
    
    # taskconfig
    task_always_eager=False,
    task_eager_propagates=True,
    
    # ENconfig
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=True,
    worker_concurrency=1,  # ENsettingsEN1，ENprocessing
    
    # resultconfig
    result_expires=3600,
    task_ignore_result=False,
    
    # taskEN
    task_routes={
        'backend.tasks.processing.*': {'queue': 'processing'},
        'backend.tasks.video.*': {'queue': 'upload'},
        'backend.tasks.notification.*': {'queue': 'notification'},
        'backend.tasks.maintenance.*': {'queue': 'maintenance'},
        'backend.tasks.upload.*': {'queue': 'upload'},
    },
    
    # taskresultconfig
    task_track_started=True,
    task_time_limit=30 * 60,  # 30EN
    task_soft_time_limit=25 * 60,  # 25EN
)

# ENtaskEN
celery_app.autodiscover_tasks([
    'backend.tasks.processing',
    'backend.tasks.video', 
    'backend.tasks.notification',
    'backend.tasks.maintenance',
    'backend.tasks.upload'
])

# ENregisterENtask，ENfailed
@celery_app.task(bind=True, name='backend.tasks.processing.process_video_pipeline')
def process_video_pipeline(self, project_id: str, input_video_path: str, input_srt_path: str):
    """videoprocessingENtask"""
    print(f"startprocessingproject: {project_id}")
    print(f"videopath: {input_video_path}")
    print(f"subtitlespath: {input_srt_path}")
    
    # ENprocessingEN
    import time
    for i in range(6):
        print(f"EN {i+1}/6: processing...")
        time.sleep(2)
    
    print(f"project {project_id} processingEN")
    return {
        "success": True,
        "project_id": project_id,
        "message": "videoprocessingEN"
    }

@celery_app.task(bind=True, name='backend.tasks.processing.process_single_step')
def process_single_step(self, project_id: str, step: str, config: dict):
    """ENprocessingtask"""
    print(f"startprocessingproject {project_id} EN: {step}")
    
    # ENprocessingEN
    import time
    time.sleep(3)
    
    print(f"EN {step} processingEN")
    return {
        "success": True,
        "project_id": project_id,
        "step": step,
        "message": f"EN {step} processingEN"
    }

@celery_app.task(bind=True, name='backend.tasks.upload.upload_to_bilibili')
def upload_to_bilibili(self, project_id: str, video_path: str, title: str, description: str):
    """uploadENBENtask"""
    print(f"startuploadproject {project_id} ENBEN")
    print(f"title: {title}")
    print(f"description: {description}")
    
    # ENuploadEN
    import time
    time.sleep(5)
    
    print(f"project {project_id} uploadEN")
    return {
        "success": True,
        "project_id": project_id,
        "message": "uploadENBEN"
    }

if __name__ == '__main__':
    celery_app.start()

