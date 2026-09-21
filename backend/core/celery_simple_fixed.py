"""
fixed'stranslatedCelerytranslateduseconfig
translatedtasktranslatedAndstatusupdateissue
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
    
    # Brokerconfig
    broker_transport='redis',
    broker_transport_options={},
    
    # translatedconfig
    task_default_queue='processing',
    task_default_exchange='processing',
    task_default_routing_key='processing',
    
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
    
    # translatedconfig
    result_expires=3600,
    task_ignore_result=False,
    
    # tasktranslatedconfig
    task_routes={
        'backend.tasks.processing.*': {'queue': 'processing'},
        'backend.tasks.video.*': {'queue': 'upload'},
        'backend.tasks.notification.*': {'queue': 'notification'},
        'backend.tasks.maintenance.*': {'queue': 'maintenance'},
        'backend.tasks.upload.*': {'queue': 'upload'},
    },
    
    # translatedusetranslated，translatedtask
    autodiscover_tasks=False,
)

# translatedtask，translated
@celery_app.task(bind=True, name='tasks.processing.process_video_pipeline')
def process_video_pipeline(self, project_id: str, input_video_path: str, input_srt_path: str, *args, **kwargs):
    """videoprocesstranslatedtask"""
    # translatedcalltranslatedprogressupdateservice'sversion
    return backend_process_video_pipeline(self, project_id, input_video_path, input_srt_path, *args, **kwargs)

@celery_app.task(bind=True, name='tasks.processing.process_single_step')
def process_single_step(self, project_id: str, step: str, config: dict, *args, **kwargs):
    """translated stepprocesstask"""
    print(f"🔧 translatedprocessproject {project_id} 'sstep: {step}")
    if args:
        print(f"⚠️  translated: {args}")
    if kwargs:
        print(f"⚠️  translated: {kwargs}")
    
    # translatedprocesstranslated
    import time
    time.sleep(3)
    
    print(f"✅ step {step} processing completed")
    return {
        "success": True,
        "project_id": project_id,
        "step": step,
        "message": f"step {step} processing completed"
    }

# translatedtasktranslated
@celery_app.task(bind=True, name='backend.tasks.processing.process_video_pipeline')
def backend_process_video_pipeline(self, project_id: str, input_video_path: str, input_srt_path: str, *args, **kwargs):
    """backendvideoprocesstranslatedtask（translated）"""
    # translatedtasktranslated，translateduseissue
    print(f"🎬 translatedprocessproject: {project_id}")
    print(f"📹 videopath: {input_video_path}")
    print(f"📝 subtitlespath: {input_srt_path}")
    if args:
        print(f"⚠️  translated: {args}")
    if kwargs:
        print(f"⚠️  translated: {kwargs}")
    
    # fetchtaskID
    task_id = self.request.id
    print(f"🔑 CelerytaskID: {task_id}")
    
    # translatedprocesstranslated
    import time
    steps = [
        "translated",
        "translated", 
        "translated",
        "translated",
        "translated",
        "videotranslated"
    ]
    
    for i, step in enumerate(steps):
        progress = (i + 1) * 16  # pertranslated16%
        print(f"📊 step {i+1}/6: {step} - {progress}%")
        
        # updatetaskstatus
        try:
            self.update_state(
                state='PROGRESS',
                meta={
                    'current': i + 1,
                    'total': 6,
                    'status': f'translatedintranslated: {step}',
                    'progress': progress
                }
            )
        except Exception as e:
            print(f"⚠️  updatetaskstatusfailed: {e}")
        
        time.sleep(2)  # translatedprocesstranslated
    
    print(f"✅ project {project_id} processing completed")
    
    # translatedupdatedatabasetranslated'staskAndprojectstatus
    try:
        from ..core.database import SessionLocal
        from ..models.task import Task, TaskStatus
        from ..models.project import Project, ProjectStatus
        from datetime import datetime
        
        # translatedupdatedatabase，translatedcallissue
        db = SessionLocal()
        try:
            # updatetaskstatus
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = TaskStatus.COMPLETED
                task.progress = 100.0
                task.current_step = 'translated'
                task.completed_at = datetime.utcnow()
                task.updated_at = datetime.utcnow()
                print(f"✅ taskstatustranslatedupdatetranslateddatabase")
            else:
                print(f"⚠️  translatedtask: {task_id}")
            
            # updateprojectstatus
            project = db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.status = ProjectStatus.COMPLETED
                project.completed_at = datetime.utcnow()
                project.updated_at = datetime.utcnow()
                print(f"✅ projectstatustranslatedupdatetranslatedcompleted: {project_id}")
            else:
                print(f"⚠️  translatedproject: {project_id}")
            
            db.commit()
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"⚠️  updatedatabasestatusfailed: {e}")
    
    return {
        "success": True,
        "project_id": project_id,
        "message": "videoprocessing completed",
        "steps": steps
    }

@celery_app.task(bind=True, name='backend.tasks.processing.process_single_step')
def backend_process_single_step(self, project_id: str, step: str, config: dict, *args, **kwargs):
    """backendtranslated stepprocesstask（translated）"""
    return process_single_step(self, project_id, step, config, *args, **kwargs)

if __name__ == '__main__':
    celery_app.start()
