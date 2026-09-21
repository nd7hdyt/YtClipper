"""
ENprocessingtask
processingvideofileuploadENtask：subtitlesgenerate、ENgenerate、processingENstart
"""

import logging
from pathlib import Path
from typing import Optional
from celery import Celery
from backend.core.database import get_db
from backend.services.project_service import ProjectService
from backend.utils.thumbnail_generator import generate_project_thumbnail
from backend.utils.task_submission_utils import submit_video_pipeline_task

logger = logging.getLogger(__name__)

# fetchCeleryEN
from backend.core.celery_app import celery_app

@celery_app.task(bind=True)
def process_import_task(self, project_id: str, video_path: str, srt_file_path: Optional[str] = None):
    """
    processingENtask
    
    Args:
        project_id: projectID
        video_path: videofilepath
        srt_file_path: subtitlesfilepath（EN）
    """
    try:
        logger.info(f"startprocessingENtask: {project_id}")
        
        # fetchdatabaseEN
        db = next(get_db())
        project_service = ProjectService(db)
        
        # checkENprojectcurrentlyprocessing（ENprocessing）
        from backend.models.task import Task, TaskStatus
        existing_task = db.query(Task).filter(
            Task.project_id == project_id,
            Task.status == TaskStatus.RUNNING,
            Task.name.like('%EN%')
        ).first()
        
        if existing_task and existing_task.celery_task_id != self.request.id:
            logger.warning(f"project {project_id} ENprocessingtaskENrun (taskID: {existing_task.celery_task_id})，ENprocessing")
            return {
                'success': False,
                'error': 'projectcurrentlyprocessing，ENprocessing',
                'existing_task_id': existing_task.celery_task_id
            }
        
        # updatetaskprogress
        self.update_state(state='PROGRESS', meta={'progress': 10, 'message': 'startprocessing...'})
        
        # 1. checkENgenerateEN（ifEN）
        logger.info(f"checkproject {project_id} EN...")
        self.update_state(state='PROGRESS', meta={'progress': 20, 'message': 'checkEN...'})
        
        project = project_service.get(project_id)
        if project and not project.thumbnail:
            logger.info(f"project {project_id} EN，startgenerate...")
            self.update_state(state='PROGRESS', meta={'progress': 25, 'message': 'generateEN...'})
            
            try:
                thumbnail_data = generate_project_thumbnail(project_id, Path(video_path))
                if thumbnail_data:
                    project.thumbnail = thumbnail_data
                    db.commit()
                    logger.info(f"project {project_id} ENgenerateENsavesucceeded")
                else:
                    logger.warning(f"project {project_id} ENgeneratefailed")
            except Exception as e:
                logger.error(f"generateprojectENerror: {e}")
                # ENgeneratefailedEN
        else:
            logger.info(f"project {project_id} EN，ENgenerate")
        
        # 2. generatesubtitles（ifEN）
        srt_path = srt_file_path
        if not srt_path:
            logger.info(f"startENproject {project_id} generatesubtitles...")
            self.update_state(state='PROGRESS', meta={'progress': 40, 'message': 'generatesubtitles...'})
            
            try:
                from backend.utils.speech_recognizer import generate_subtitle_for_video
                from backend.core.desktop_config import get_desktop_config
                
                # fetchuserconfigENtranscriptionsettings
                config = get_desktop_config()
                speech_config = config.speech_recognition
                
                logger.info(f"useENtranscriptionconfig - EN: {speech_config.method}")
                
                # ENconfigENparameters
                if speech_config.method == "whisper_local":
                    # useuserconfigENWhisperparameters
                    model = speech_config.whisper_config.model_name
                    language = speech_config.whisper_config.language
                    enable_timestamps = speech_config.whisper_config.enable_timestamps
                    enable_punctuation = speech_config.whisper_config.enable_punctuation
                    enable_speaker_diarization = speech_config.whisper_config.enable_speaker_diarization
                    timeout = speech_config.whisper_config.timeout
                    
                    logger.info(f"Whisperconfig - EN: {model}, EN: {language}, timeEN: {enable_timestamps}")
                    
                    generated_subtitle = generate_subtitle_for_video(
                        Path(video_path),
                        language=language,
                        model=model,
                        method=speech_config.method,
                        enable_timestamps=enable_timestamps,
                        enable_punctuation=enable_punctuation,
                        enable_speaker_diarization=enable_speaker_diarization,
                        timeout=timeout
                    )
                else:
                    # useAPIservice
                    logger.info(f"useAPIservice - {speech_config.method}")
                    
                    # ENserviceENfetchAPIconfig
                    if speech_config.method == "openai_api":
                        api_config = speech_config.openai_config
                    elif speech_config.method == "azure_speech":
                        api_config = speech_config.azure_config
                    elif speech_config.method == "google_speech":
                        api_config = speech_config.google_config
                    elif speech_config.method == "aliyun_speech":
                        api_config = speech_config.aliyun_config
                    elif speech_config.method == "custom_api":
                        api_config = speech_config.custom_api_config
                    else:
                        raise ValueError(f"EN: {speech_config.method}")
                    
                    generated_subtitle = generate_subtitle_for_video(
                        Path(video_path),
                        method=speech_config.method,
                        language=api_config.language,
                        api_key=api_config.api_key,
                        enable_timestamps=api_config.enable_timestamps,
                        enable_punctuation=api_config.enable_punctuation
                    )
                
                srt_path = str(generated_subtitle)
                logger.info(f"ENtranscriptionsucceeded: {srt_path}")
                
            except Exception as e:
                logger.error(f"ENtranscriptionfailed: {str(e)}")
                
                # ifEN，ENuseEN
                if speech_config.enable_fallback and speech_config.fallback_method != speech_config.method:
                    try:
                        logger.info(f"EN: {speech_config.fallback_method}")
                        
                        if speech_config.fallback_method == "whisper_local":
                            fallback_config = speech_config.whisper_config
                            generated_subtitle = generate_subtitle_for_video(
                                Path(video_path),
                                language=fallback_config.language,
                                model=fallback_config.model_name,
                                method=speech_config.fallback_method
                            )
                        else:
                            # EN
                            generated_subtitle = generate_subtitle_for_video(
                                Path(video_path),
                                method=speech_config.fallback_method
                            )
                        
                        srt_path = str(generated_subtitle)
                        logger.info(f"ENsucceeded: {srt_path}")
                        
                    except Exception as fallback_error:
                        logger.error(f"ENfailed: {str(fallback_error)}")
                        srt_path = None
                else:
                    srt_path = None
        
        # 3. updateprojectstatusENprocessing
        logger.info(f"updateproject {project_id} statusENprocessing...")
        self.update_state(state='PROGRESS', meta={'progress': 80, 'message': 'startprocessingEN...'})
        
        project_service.update_project_status(project_id, "processing")
        
        # 4. startprocessingEN
        if srt_path and Path(srt_path).exists():
            try:
                task_result = submit_video_pipeline_task(
                    project_id=project_id,
                    input_video_path=video_path,
                    input_srt_path=srt_path
                )
                
                if task_result['success']:
                    logger.info(f"project {project_id} processingtaskENstart，CelerytaskID: {task_result['task_id']}")
                    self.update_state(state='PROGRESS', meta={'progress': 100, 'message': 'processingENstart'})
                else:
                    logger.error(f"CelerytaskENfailed: {task_result['error']}")
                    project_service.update_project_status(project_id, "failed")
                    self.update_state(state='FAILURE', meta={'error': task_result['error']})
                    return
                    
            except Exception as e:
                logger.error(f"startproject {project_id} processingfailed: {str(e)}")
                project_service.update_project_status(project_id, "failed")
                self.update_state(state='FAILURE', meta={'error': str(e)})
                return
        else:
            logger.error(f"subtitlesfiledoes not exist: {srt_path}")
            project_service.update_project_status(project_id, "failed")
            self.update_state(state='FAILURE', meta={'error': 'subtitlesfiledoes not exist'})
            return
        
        logger.info(f"ENtaskEN: {project_id}")
        return {
            'status': 'completed',
            'project_id': project_id,
            'message': 'ENprocessingEN'
        }
        
    except Exception as e:
        logger.error(f"ENtaskfailed: {project_id}, error: {e}")
        
        # updateprojectstatusENfailed
        try:
            db = next(get_db())
            project_service = ProjectService(db)
            project_service.update_project_status(project_id, "failed")
        except:
            pass
        
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise
    finally:
        try:
            db.close()
        except:
            pass

