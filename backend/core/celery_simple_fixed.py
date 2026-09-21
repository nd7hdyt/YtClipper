"""
ENCeleryENconfig
ENtaskENstatusupdateEN
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
    
    # Brokerconfig
    broker_transport='redis',
    broker_transport_options={},
    
    # queueconfig
    task_default_queue='processing',
    task_default_exchange='processing',
    task_default_routing_key='processing',
    
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
    
    # taskENconfig
    task_routes={
        'backend.tasks.processing.*': {'queue': 'processing'},
        'backend.tasks.video.*': {'queue': 'upload'},
        'backend.tasks.notification.*': {'queue': 'notification'},
        'backend.tasks.maintenance.*': {'queue': 'maintenance'},
        'backend.tasks.upload.*': {'queue': 'upload'},
    },
    
    # EN，ENregistertask
    autodiscover_tasks=False,
)

# ENregistertask，EN
@celery_app.task(bind=True, name='tasks.processing.process_video_pipeline')
def process_video_pipeline(self, project_id: str, input_video_path: str, input_srt_path: str, *args, **kwargs):
    """videoprocessingENtask"""
    # ENcallENprogressupdateserviceEN
    return backend_process_video_pipeline(self, project_id, input_video_path, input_srt_path, *args, **kwargs)

@celery_app.task(bind=True, name='tasks.processing.process_single_step')
def process_single_step(self, project_id: str, step: str, config: dict, *args, **kwargs):
    """ENprocessingtask"""
    print(f"🔧 startprocessingproject {project_id} EN: {step}")
    if args:
        print(f"⚠️  ENparameters: {args}")
    if kwargs:
        print(f"⚠️  ENparameters: {kwargs}")
    
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
def backend_process_video_pipeline(self, project_id: str, input_video_path: str, input_srt_path: str, *args, **kwargs):
    """ENvideoprocessingENtask（EN）"""
    # ENtaskEN，EN
    print(f"🎬 startprocessingproject: {project_id}")
    print(f"📹 videopath: {input_video_path}")
    print(f"📝 subtitlespath: {input_srt_path}")
    if args:
        print(f"⚠️  ENparameters: {args}")
    if kwargs:
        print(f"⚠️  ENparameters: {kwargs}")
    
    # fetchtaskID
    task_id = self.request.id
    print(f"🔑 CelerytaskID: {task_id}")
    
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
        try:
            self.update_state(
                state='PROGRESS',
                meta={
                    'current': i + 1,
                    'total': 6,
                    'status': f'currentlyexecute: {step}',
                    'progress': progress
                }
            )
        except Exception as e:
            print(f"⚠️  updatetaskstatusfailed: {e}")
        
        time.sleep(2)  # ENprocessingtime
    
    print(f"✅ project {project_id} processingEN")
    
    # ENupdatedatabaseENtaskENprojectstatus
    try:
        from ..core.database import SessionLocal
        from ..models.task import Task, TaskStatus
        from ..models.project import Project, ProjectStatus
        from datetime import datetime
        
        # ENupdatedatabase，ENcallEN
        db = SessionLocal()
        try:
            # updatetaskstatus
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = TaskStatus.COMPLETED
                task.progress = 100.0
                task.current_step = 'EN'
                task.completed_at = datetime.utcnow()
                task.updated_at = datetime.utcnow()
                print(f"✅ taskstatusupdatedENdatabase")
            else:
                print(f"⚠️  ENtask: {task_id}")
            
            # updateprojectstatus
            project = db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.status = ProjectStatus.COMPLETED
                project.completed_at = datetime.utcnow()
                project.updated_at = datetime.utcnow()
                print(f"✅ projectstatusupdatedENcompleted: {project_id}")
            else:
                print(f"⚠️  ENproject: {project_id}")
            
            db.commit()
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"⚠️  updatedatabasestatusfailed: {e}")
    
    return {
        "success": True,
        "project_id": project_id,
        "message": "videoprocessingEN",
        "steps": steps
    }

@celery_app.task(bind=True, name='backend.tasks.processing.process_single_step')
def backend_process_single_step(self, project_id: str, step: str, config: dict, *args, **kwargs):
    """ENprocessingtask（EN）"""
    return process_single_step(self, project_id, step, config, *args, **kwargs)

if __name__ == '__main__':
    celery_app.start()
