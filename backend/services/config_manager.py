"""
projectconfigtranslated
translatedper project'sconfiginfo，Packagetranslatedpromptfile、APIkey、processtranslatedetc.
"""

import os
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from ..models.project import ProjectType
from ..core.database import get_db

logger = logging.getLogger(__name__)


class ProcessingStep(str, Enum):
    """processsteptranslated"""
    STEP1_OUTLINE = "step1_outline"
    STEP2_TIMELINE = "step2_timeline"
    STEP3_SCORING = "step3_scoring"
    STEP4_TITLE = "step4_title"
    STEP5_CLUSTERING = "step5_clustering"
    STEP6_VIDEO = "step6_video"


@dataclass
class LLMConfig:
    """LLMconfig"""
    api_key: str
    model_name: str = "qwen-plus"
    max_retries: int = 3
    timeout_seconds: int = 30


@dataclass
class ProcessingParams:
    """processtranslated"""
    chunk_size: int = 5000
    min_score_threshold: float = 0.7
    max_clips_per_collection: int = 5
    min_topic_duration_minutes: int = 2
    max_topic_duration_minutes: int = 12
    target_topic_duration_minutes: int = 5
    min_topics_per_chunk: int = 3
    max_topics_per_chunk: int = 8


class ProjectConfigManager:
    """projectconfigtranslated"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_dir = Path(f"data/projects/{project_id}")
        self.config_path = self.project_dir / "config.yaml"
        # usetranslatedpathtranslatedprojecttranslateddirectory'spromptfiletranslated
        project_root = Path(__file__).parent.parent.parent
        self.prompt_dir = Path(__file__).parent.parent / "prompt"
        
        # ensureprojectdirectorytranslatedin
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # translatedconfig
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """translatedprojectconfig"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config is None:
                        logger.warning(f"configfiletranslated: {self.config_path}")
                        return {}
                    return config
            except yaml.YAMLError as e:
                logger.error(f"YAMLtranslatederror: {self.config_path}, error: {e}")
                return {}
            except FileNotFoundError as e:
                logger.error(f"configfile not found: {self.config_path}, error: {e}")
                return {}
            except Exception as e:
                logger.error(f"translatedprojectconfigfailed: {self.config_path}, error: {e}")
                return {}
        return {}
    
    def _save_config(self):
        """translatedprojectconfig"""
        try:
            # ensuredirectorytranslatedin
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"configtranslated: {self.config_path}")
        except Exception as e:
            logger.error(f"translatedprojectconfigfailed: {self.config_path}, error: {e}")
            raise
    
    def get_prompt_files(self, project_type: str = "default", language: str = "zh") -> Dict[str, Path]:
        """
        fetchprojecttranslated'spromptfile path
        
        Args:
            project_type: projecttranslated，translated'sprompttranslated
            language: Languageversion，supportmultiLanguageprompt
            
        Returns:
            promptfile pathtranslated
        """
        # fromconfigtranslatedfetchpromptsettings
        prompt_config = self.config.get("prompts", {})
        
        # translatedpromptfile
        base_prompts = {
            "outline": self.prompt_dir / "translated.txt",
            "timeline": self.prompt_dir / "translated.txt",
            "recommendation": self.prompt_dir / "recommendtranslated.txt",
            "title": self.prompt_dir / "translated.txt",
            "clustering": self.prompt_dir / "translated.txt"
        }
        
        # iftranslatedconfigtranslatedpromptpath，useconfig'spath
        if "custom_paths" in prompt_config:
            for key, custom_path in prompt_config["custom_paths"].items():
                if key in base_prompts:
                    custom_file = Path(custom_path)
                    if custom_file.exists():
                        base_prompts[key] = custom_file
                        logger.info(f"usetranslatedprompt: {key} -> {custom_path}")
        
        # checkprojecttranslated'spromptfile
        type_prompt_dir = self.prompt_dir / project_type
        if type_prompt_dir.exists():
            for key in base_prompts:
                type_specific_prompt = type_prompt_dir / f"{key}.txt"
                if type_specific_prompt.exists():
                    base_prompts[key] = type_specific_prompt
                    logger.info(f"useprojecttranslatedprompt: {key} -> {type_specific_prompt}")
        
        # checkmultiLanguagepromptfile
        if language != "zh":
            lang_prompt_dir = self.prompt_dir / "languages" / language
            if lang_prompt_dir.exists():
                for key in base_prompts:
                    lang_specific_prompt = lang_prompt_dir / f"{key}.txt"
                    if lang_specific_prompt.exists():
                        base_prompts[key] = lang_specific_prompt
                        logger.info(f"usemultiLanguageprompt: {key} -> {lang_specific_prompt}")
        
        # verifytranslatedpromptfileIstranslatedin
        missing_prompts = []
        for key, path in base_prompts.items():
            if not path.exists():
                missing_prompts.append(f"{key}: {path}")
        
        if missing_prompts:
            logger.warning(f"translatedpromptfile: {missing_prompts}")
        
        return base_prompts
    
    def get_llm_config(self) -> LLMConfig:
        """fetchLLMconfig"""
        # translatedfromprojectconfigfetch
        llm_config = self.config.get("llm", {})
        
        # APIkeytranslated：projectconfig > translated > defaulttranslated
        api_key = llm_config.get("api_key") or os.getenv("DASHSCOPE_API_KEY", "")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY translatedinprojectconfigortranslatedsettings")
        
        return LLMConfig(
            api_key=api_key,
            model_name=llm_config.get("model_name", "qwen-plus"),
            max_retries=llm_config.get("max_retries", 3),
            timeout_seconds=llm_config.get("timeout_seconds", 30)
        )
    
    def get_processing_params(self) -> ProcessingParams:
        """fetchprocesstranslated"""
        params = self.config.get("processing_params", {})
        return ProcessingParams(
            chunk_size=params.get("chunk_size", 5000),
            min_score_threshold=params.get("min_score_threshold", 0.7),
            max_clips_per_collection=params.get("max_clips_per_collection", 5),
            min_topic_duration_minutes=params.get("min_topic_duration_minutes", 2),
            max_topic_duration_minutes=params.get("max_topic_duration_minutes", 12),
            target_topic_duration_minutes=params.get("target_topic_duration_minutes", 5),
            min_topics_per_chunk=params.get("min_topics_per_chunk", 3),
            max_topics_per_chunk=params.get("max_topics_per_chunk", 8)
        )
    
    def update_processing_params(self, **kwargs):
        """updateprocesstranslated"""
        if "processing_params" not in self.config:
            self.config["processing_params"] = {}
        
        self.config["processing_params"].update(kwargs)
        self._save_config()
    
    def update_llm_config(self, **kwargs):
        """updateLLMconfig"""
        if "llm" not in self.config:
            self.config["llm"] = {}
        
        self.config["llm"].update(kwargs)
        self._save_config()
    
    def get_project_paths(self) -> Dict[str, Path]:
        """fetchprojecttranslatedpath"""
        return {
            "project_dir": self.project_dir,
            "metadata_dir": self.project_dir / "metadata",
            "raw_dir": self.project_dir / "raw",
            "outputs_dir": self.project_dir / "outputs",
            "logs_dir": self.project_dir / "logs"
        }
    
    def ensure_project_directories(self):
        """ensureprojectdirectorytranslatedin"""
        paths = self.get_project_paths()
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)
    
    def get_step_config(self, step_name: str) -> Dict[str, Any]:
        """fetchtranslatedstep'sconfig"""
        step_configs = self.config.get("steps", {})
        return step_configs.get(step_name, {})
    
    def update_step_config(self, step_name: str, **kwargs):
        """updatetranslatedstep'sconfig"""
        if "steps" not in self.config:
            self.config["steps"] = {}
        
        if step_name not in self.config["steps"]:
            self.config["steps"][step_name] = {}
        
        self.config["steps"][step_name].update(kwargs)
        self._save_config()
    
    def backup_config(self, backup_path: Optional[Path] = None) -> Path:
        """translatedconfig"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.project_dir / f"config_backup_{timestamp}.yaml"
        
        try:
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            with open(backup_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"configtranslated: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"configtranslatedfailed: {e}")
            raise
    
    def restore_config(self, backup_path: Path) -> bool:
        """fromtranslatedconfig"""
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_config = yaml.safe_load(f)
            
            if backup_config is None:
                raise ValueError("translatedfiletranslated")
            
            # translatedconfig
            self.backup_config()
            
            # translatedconfig
            self.config = backup_config
            self._save_config()
            
            logger.info(f"configtranslatedfromtranslated: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"configtranslatedfailed: {e}")
            return False
    
    def export_config(self) -> Dict[str, Any]:
        """exportconfig"""
        return {
            "project_id": self.project_id,
            "llm_config": {
                "api_key": self.get_llm_config().api_key,
                "model_name": self.get_llm_config().model_name,
                "max_retries": self.get_llm_config().max_retries,
                "timeout_seconds": self.get_llm_config().timeout_seconds
            },
            "processing_params": {
                "chunk_size": self.get_processing_params().chunk_size,
                "min_score_threshold": self.get_processing_params().min_score_threshold,
                "max_clips_per_collection": self.get_processing_params().max_clips_per_collection,
                "min_topic_duration_minutes": self.get_processing_params().min_topic_duration_minutes,
                "max_topic_duration_minutes": self.get_processing_params().max_topic_duration_minutes,
                "target_topic_duration_minutes": self.get_processing_params().target_topic_duration_minutes,
                "min_topics_per_chunk": self.get_processing_params().min_topics_per_chunk,
                "max_topics_per_chunk": self.get_processing_params().max_topics_per_chunk
            },
            "project_paths": self.get_project_paths(),
            "prompt_files": self.get_prompt_files()
        }
    
    def get_project_config(self) -> Dict[str, Any]:
        """fetchprojectconfig"""
        # translatedfromdatabasefetchprojectconfig
        try:
            from sqlalchemy.orm import Session
            from ..core.database import SessionLocal
            from ..models.project import Project
            
            db = SessionLocal()
            try:
                project = db.query(Project).filter(Project.id == self.project_id).first()
                if project and project.processing_config:
                    return project.processing_config
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"translatedfromdatabasefetchprojectconfig: {e}")
        
        # translatedlocalconfigfile
        return self.config
    
    def validate_config(self) -> Dict[str, Any]:
        """verifyconfig'stranslatedAndtranslated"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "missing_files": []
        }
        
        # verifyLLMconfig
        try:
            self.get_llm_config()
        except ValueError as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"LLMconfigerror: {e}")
        
        # verifypromptfile
        prompt_files = self.get_prompt_files()
        for key, path in prompt_files.items():
            if not path.exists():
                validation_result["warnings"].append(f"Promptfile not found: {key} -> {path}")
                validation_result["missing_files"].append(str(path))
        
        # verifyprojectdirectory
        project_paths = self.get_project_paths()
        for key, path in project_paths.items():
            if not path.exists():
                validation_result["warnings"].append(f"projectdirectorynot found: {key} -> {path}")
        
        # verifyprocesstranslated
        try:
            params = self.get_processing_params()
            if params.chunk_size <= 0:
                validation_result["errors"].append("chunk_sizetranslated0")
            if params.min_score_threshold < 0 or params.min_score_threshold > 1:
                validation_result["errors"].append("min_score_thresholdtranslatedin0-1translated")
        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"processtranslatederror: {e}")
        
        if validation_result["errors"]:
            validation_result["valid"] = False
        
        return validation_result