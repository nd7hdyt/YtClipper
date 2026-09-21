"""
ENCeleryENconfig
ENallEN，ENtaskprocessingEN
"""

import os
import sys
from pathlib import Path
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
    
    # resultconfig
    result_expires=3600,
    task_ignore_result=False,
    
    # EN
    autodiscover_tasks=False,
)

# ENregistertask
@celery_app.task(bind=True, name='tasks.processing.process_video_pipeline')
def process_video_pipeline(self, project_id: str, input_video_path: str, input_srt_path: str):
    """videoprocessingENtask"""
    print(f"🎬 startprocessingproject: {project_id}")
    print(f"📹 videopath: {input_video_path}")
    print(f"📝 subtitlespath: {input_srt_path}")
    
    # ENprocessingEN
    import time
    steps = [
        "EN",
        "timeEN", 
        "ENscoring",
        "titlegenerate",
        "EN",
        "videoEN"
    ]
    
    for i, step in enumerate(steps):
        progress = (i + 1) * 16  # EN16%
        print(f"📊 EN {i+1}/6: {step} - {progress}%")
        
        # updatetaskstatus
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i + 1,
                'total': 6,
                'status': f'currentlyexecute: {step}',
                'progress': progress
            }
        )
        
        time.sleep(2)  # ENprocessingtime
    
    print(f"✅ project {project_id} processingEN")
    return {
        "success": True,
        "project_id": project_id,
        "message": "videoprocessingEN",
        "steps": steps
    }

@celery_app.task(bind=True, name='tasks.processing.process_single_step')
def process_single_step(self, project_id: str, step: str, config: dict):
    """ENprocessingtask"""
    print(f"🔧 startprocessingproject {project_id} EN: {step}")
    
    # ENprocessingEN
    import time
    time.sleep(3)
    
    print(f"✅ EN {step} processingEN")
    return {
        "success": True,
        "project_id": project_id,
        "step": step,
        "message": f"EN {step} processingEN"
    }

# ENtaskEN
@celery_app.task(bind=True, name='backend.tasks.processing.process_video_pipeline')
def backend_process_video_pipeline(self, project_id: str, input_video_path: str, input_srt_path: str):
    """ENvideoprocessingENtask（EN）"""
    return process_video_pipeline(self, project_id, input_video_path, input_srt_path)

@celery_app.task(bind=True, name='backend.tasks.processing.process_single_step')
def backend_process_single_step(self, project_id: str, step: str, config: dict):
    """ENprocessingtask（EN）"""
    return process_single_step(self, project_id, step, config)

if __name__ == '__main__':
    celery_app.start()

