"""
translatedone'sCelerytranslateduseconfig
translatedimportissue，Providestranslated'stasktranslated
"""

import os
from celery import Celery

# createCelerytranslateduse
celery_app = Celery('autoclip')

# translatedconfig
celery_app.conf.update(
    # translatedformat
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Redisconfig
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    
    # translated
    timezone='Asia/Shanghai',
    enable_utc=True,
    
    # taskconfig
    task_always_eager=False,
    task_eager_propagates=True,
    
    # translatedprocessconfig
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=True,
    worker_concurrency=1,  # translatedsettingstranslated1，translatedprocess
    
    # translatedconfig
    result_expires=3600,
    task_ignore_result=False,
    
    # tasktranslated
    task_routes={
        'backend.tasks.processing.*': {'queue': 'processing'},
        'backend.tasks.video.*': {'queue': 'upload'},
        'backend.tasks.notification.*': {'queue': 'notification'},
        'backend.tasks.maintenance.*': {'queue': 'maintenance'},
        'backend.tasks.upload.*': {'queue': 'upload'},
    },
    
    # tasktranslatedconfig
    task_track_started=True,
    task_time_limit=30 * 60,  # 30minutes
    task_soft_time_limit=25 * 60,  # 25minutes
)

# translatedtasktranslated
celery_app.autodiscover_tasks([
    'backend.tasks.processing',
    'backend.tasks.video', 
    'backend.tasks.notification',
    'backend.tasks.maintenance',
    'backend.tasks.upload'
])

# translatedtask，translatedfailed
@celery_app.task(bind=True, name='backend.tasks.processing.process_video_pipeline')
def process_video_pipeline(self, project_id: str, input_video_path: str, input_srt_path: str):
    """videoprocesstranslatedtask"""
    print(f"translatedprocessproject: {project_id}")
    print(f"videopath: {input_video_path}")
    print(f"subtitlespath: {input_srt_path}")
    
    # translatedprocesstranslated
    import time
    for i in range(6):
        print(f"step {i+1}/6: processing...")
        time.sleep(2)
    
    print(f"project {project_id} processing completed")
    return {
        "success": True,
        "project_id": project_id,
        "message": "videoprocessing completed"
    }

@celery_app.task(bind=True, name='backend.tasks.processing.process_single_step')
def process_single_step(self, project_id: str, step: str, config: dict):
    """translated stepprocesstask"""
    print(f"translatedprocessproject {project_id} 'sstep: {step}")
    
    # translatedprocesstranslated
    import time
    time.sleep(3)
    
    print(f"step {step} processing completed")
    return {
        "success": True,
        "project_id": project_id,
        "step": step,
        "message": f"step {step} processing completed"
    }

@celery_app.task(bind=True, name='backend.tasks.upload.upload_to_bilibili')
def upload_to_bilibili(self, project_id: str, video_path: str, title: str, description: str):
    """UploadtranslatedBsitetask"""
    print(f"translatedUploadproject {project_id} translatedBsite")
    print(f"translated: {title}")
    print(f"translated: {description}")
    
    # translatedUploadtranslated
    import time
    time.sleep(5)
    
    print(f"project {project_id} Uploadtranslated")
    return {
        "success": True,
        "project_id": project_id,
        "message": "UploadtranslatedBsitetranslated"
    }

if __name__ == '__main__':
    celery_app.start()

