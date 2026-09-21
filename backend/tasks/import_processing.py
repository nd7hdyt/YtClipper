"""
localimportprocesstask
processvideofileUploadtranslated'stranslatedtask：subtitlestranslated、translated、processtranslatedstart
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

# fetchCelerytranslatedusetranslated
from backend.core.celery_app import celery_app

@celery_app.task(bind=True)
def process_import_task(self, project_id: str, video_path: str, srt_file_path: Optional[str] = None):
    """
    processlocalimport'stranslatedtask
    
    Args:
        project_id: projectID
        video_path: videofile path
        srt_file_path: subtitlesfile path（canSelect）
    """
    try:
        logger.info(f"translatedprocessimporttask: {project_id}")
        
        # fetchdatabasetranslated
        db = next(get_db())
        project_service = ProjectService(db)
        
        # checkIstranslatedprojecttranslatedinprocessing（translatedprocess）
        from backend.models.task import Task, TaskStatus
        existing_task = db.query(Task).filter(
            Task.project_id == project_id,
            Task.status == TaskStatus.RUNNING,
            Task.name.like('%import%')
        ).first()
        
        if existing_task and existing_task.celery_task_id != self.request.id:
            logger.warning(f"project {project_id} translatedprocesstaskintranslated (taskID: {existing_task.celery_task_id})，skiptranslatedprocess")
            return {
                'success': False,
                'error': 'projecttranslatedinprocessing，translatedprocess',
                'existing_task_id': existing_task.celery_task_id
            }
        
        # updatetaskprogress
        self.update_state(state='PROGRESS', meta={'progress': 10, 'message': 'translatedprocess...'})
        
        # 1. checktranslated（iftranslated）
        logger.info(f"checkproject {project_id} translated...")
        self.update_state(state='PROGRESS', meta={'progress': 20, 'message': 'checktranslated...'})
        
        project = project_service.get(project_id)
        if project and not project.thumbnail:
            logger.info(f"project {project_id} translated，translated...")
            self.update_state(state='PROGRESS', meta={'progress': 25, 'message': 'translated...'})
            
            try:
                thumbnail_data = generate_project_thumbnail(project_id, Path(video_path))
                if thumbnail_data:
                    project.thumbnail = thumbnail_data
                    db.commit()
                    logger.info(f"project {project_id} translatedsucceeded")
                else:
                    logger.warning(f"project {project_id} translatedfailed")
            except Exception as e:
                logger.error(f"translatedprojecttranslatederror: {e}")
                # translatedfailedtranslated
        else:
            logger.info(f"project {project_id} translated，skiptranslated")
        
        # 2. generate subtitles（iftranslatedProvides）
        srt_path = srt_file_path
        if not srt_path:
            logger.info(f"translatedproject {project_id} generate subtitles...")
            self.update_state(state='PROGRESS', meta={'progress': 40, 'message': 'generate subtitles...'})
            
            try:
                from backend.utils.speech_recognizer import generate_subtitle_for_video
                from backend.core.desktop_config import get_desktop_config
                
                # fetchuserconfig'stranslatedsettings
                config = get_desktop_config()
                speech_config = config.speech_recognition
                
                logger.info(f"usetranslatedconfig - translated: {speech_config.method}")
                
                # translatedconfigSelectselecttranslated
                if speech_config.method == "whisper_local":
                    # useuserconfig'sWhispertranslated
                    model = speech_config.whisper_config.model_name
                    language = speech_config.whisper_config.language
                    enable_timestamps = speech_config.whisper_config.enable_timestamps
                    enable_punctuation = speech_config.whisper_config.enable_punctuation
                    enable_speaker_diarization = speech_config.whisper_config.enable_speaker_diarization
                    timeout = speech_config.whisper_config.timeout
                    
                    logger.info(f"Whisperconfig - model: {model}, Language: {language}, translated: {enable_timestamps}")
                    
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
                    
                    # translatedservicetranslatedfetchAPIconfig
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
                        raise ValueError(f"translatedsupport'stranslated: {speech_config.method}")
                    
                    generated_subtitle = generate_subtitle_for_video(
                        Path(video_path),
                        method=speech_config.method,
                        language=api_config.language,
                        api_key=api_config.api_key,
                        enable_timestamps=api_config.enable_timestamps,
                        enable_punctuation=api_config.enable_punctuation
                    )
                
                srt_path = str(generated_subtitle)
                logger.info(f"translatedsucceeded: {srt_path}")
                
            except Exception as e:
                logger.error(f"translatedfailed: {str(e)}")
                
                # iftranslatedusetranslated，translatedusetranslated
                if speech_config.enable_fallback and speech_config.fallback_method != speech_config.method:
                    try:
                        logger.info(f"translated: {speech_config.fallback_method}")
                        
                        if speech_config.fallback_method == "whisper_local":
                            fallback_config = speech_config.whisper_config
                            generated_subtitle = generate_subtitle_for_video(
                                Path(video_path),
                                language=fallback_config.language,
                                model=fallback_config.model_name,
                                method=speech_config.fallback_method
                            )
                        else:
                            # translated
                            generated_subtitle = generate_subtitle_for_video(
                                Path(video_path),
                                method=speech_config.fallback_method
                            )
                        
                        srt_path = str(generated_subtitle)
                        logger.info(f"translatedsucceeded: {srt_path}")
                        
                    except Exception as fallback_error:
                        logger.error(f"translatedfailed: {str(fallback_error)}")
                        srt_path = None
                else:
                    srt_path = None
        
        # 3. updateprojectstatustranslatedprocessing
        logger.info(f"updateproject {project_id} statustranslatedprocessing...")
        self.update_state(state='PROGRESS', meta={'progress': 80, 'message': 'startprocesstranslated...'})
        
        project_service.update_project_status(project_id, "processing")
        
        # 4. startprocesstranslated
        if srt_path and Path(srt_path).exists():
            try:
                task_result = submit_video_pipeline_task(
                    project_id=project_id,
                    input_video_path=video_path,
                    input_srt_path=srt_path
                )
                
                if task_result['success']:
                    logger.info(f"project {project_id} processtasktranslatedstart，CelerytaskID: {task_result['task_id']}")
                    self.update_state(state='PROGRESS', meta={'progress': 100, 'message': 'processtranslatedstart'})
                else:
                    logger.error(f"Celerytasktranslatedfailed: {task_result['error']}")
                    project_service.update_project_status(project_id, "failed")
                    self.update_state(state='FAILURE', meta={'error': task_result['error']})
                    return
                    
            except Exception as e:
                logger.error(f"startproject {project_id} processing failed: {str(e)}")
                project_service.update_project_status(project_id, "failed")
                self.update_state(state='FAILURE', meta={'error': str(e)})
                return
        else:
            logger.error(f"subtitlesfile not found: {srt_path}")
            project_service.update_project_status(project_id, "failed")
            self.update_state(state='FAILURE', meta={'error': 'subtitlesfile not found'})
            return
        
        logger.info(f"importtasktranslated: {project_id}")
        return {
            'status': 'completed',
            'project_id': project_id,
            'message': 'importprocessing completed'
        }
        
    except Exception as e:
        logger.error(f"importtaskfailed: {project_id}, error: {e}")
        
        # updateprojectstatustranslatedfailed
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

