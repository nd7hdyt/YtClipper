"""
Step 5: translated - translatedcollection
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

# importdependencies
from ..utils.llm_client import LLMClient
from ..core.shared_config import PROMPT_FILES, METADATA_DIR, MAX_CLIPS_PER_COLLECTION

logger = logging.getLogger(__name__)

class ClusteringEngine:
    """translated"""
    
    def __init__(self, metadata_dir: Optional[Path] = None, prompt_files: Dict = None):
        self.llm_client = LLMClient()
        
        # translated
        prompt_files_to_use = prompt_files if prompt_files is not None else PROMPT_FILES
        with open(prompt_files_to_use['clustering'], 'r', encoding='utf-8') as f:
            self.clustering_prompt = f.read()
        
        # usetranslated'smetadata_dirordefaulttranslated
        if metadata_dir is None:
            metadata_dir = METADATA_DIR
        self.metadata_dir = metadata_dir
    
    def cluster_clips(self, clips_with_titles: List[Dict]) -> List[Dict]:
        """
        translated
        
        Args:
            clips_with_titles: translated'stranslatedlist
            
        Returns:
            collectiontranslatedlist
        """
        logger.info("translated...")
        
        # translated
        clips_for_clustering = []
        for clip in clips_with_titles:
            clips_for_clustering.append({
                'id': clip['id'],
                'title': clip.get('generated_title', clip['outline']),
                'summary': clip.get('recommend_reason', ''),
                'score': clip.get('final_score', 0)
            })
        
        # translatedBased ontranslated'stranslated
        pre_clusters = self._pre_cluster_by_keywords(clips_for_clustering)
        
        # translated'stranslated
        full_prompt = self.clustering_prompt + "\n\ntranslatedIsvideocliplist：\n"
        for i, clip in enumerate(clips_for_clustering, 1):
            full_prompt += f"{i}. translated：{clip['title']}\n   translated：{clip['summary']}\n   translated：{clip['score']:.2f}\n\n"
        
        # addtranslatedReference
        if pre_clusters:
            full_prompt += "\n\nBased ontranslated'stranslated（OnlytranslatedReference）：\n"
            for theme, clip_ids in pre_clusters.items():
                full_prompt += f"{theme}: {', '.join(clip_ids)}\n"
        
        try:
            # calltranslatedmodeltranslated
            response = self.llm_client.call_with_retry(full_prompt)
            
            # translatedJSONtranslated
            collections_data = self.llm_client.parse_json_response(response)
            
            # verifyAndcleancollectiontranslated
            validated_collections = self._validate_collections(collections_data, clips_with_titles)
            
            # iftranslatedLLMtranslated，usetranslated
            if len(validated_collections) < 3:
                logger.warning("LLMtranslated，usetranslated")
                validated_collections = self._create_collections_from_pre_clusters(pre_clusters, clips_with_titles)
            
            logger.info(f"translated，translated{len(validated_collections)} collection")
            return validated_collections
            
        except Exception as e:
            logger.error(f"translatedfailed: {str(e)}")
            # usetranslatedSelect
            if pre_clusters:
                logger.info("usetranslatedSelecttranslated")
                return self._create_collections_from_pre_clusters(pre_clusters, clips_with_titles)
            # returndefaulttranslated
            return self._create_default_collections(clips_with_titles)
    
    def _pre_cluster_by_keywords(self, clips: List[Dict]) -> Dict[str, List[str]]:
        """
        Based ontranslated
        
        Args:
            clips: translatedlist
            
        Returns:
            translated
        """
        # translated
        theme_keywords = {
            'translated': ['translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'Atranslated', 'translated', 'translated', 'translated'],
            'translated': ['translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translatedprovider'],
            'translated': ['translated', 'Symptom', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated'],
            'translated': ['translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'Language', 'translated', 'translated', 'translated'],
            'translated': ['translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'PK', 'translated'],
            'translated': ['translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated'],
            'translated': ['translated', 'translated', 'translated', 'translated', 'translated', 'translated', 'translated'],
            'translated': ['translated', 'translated', 'Bsite', 'translated', 'translated', 'translated', 'translated', 'translated']
        }
        
        pre_clusters = {theme: [] for theme in theme_keywords.keys()}
        
        for clip in clips:
            # translatedAndtranslated
            text = f"{clip['title']} {clip['summary']}".lower()
            
            # translatedper translated'stranslated
            theme_scores = {}
            for theme, keywords in theme_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text)
                if score > 0:
                    theme_scores[theme] = score
            
            # Selectselecttranslated'stranslated
            if theme_scores:
                best_theme = max(theme_scores.keys(), key=lambda k: theme_scores[k])
                pre_clusters[best_theme].append(clip['id'])
        
        # translated'stranslated
        return {theme: clip_ids for theme, clip_ids in pre_clusters.items() if len(clip_ids) >= 2}
    
    def _create_collections_from_pre_clusters(self, pre_clusters: Dict[str, List[str]], clips_with_titles: List[Dict]) -> List[Dict]:
        """
        fromtranslatedcreatecollection
        
        Args:
            pre_clusters: translated
            clips_with_titles: translated
            
        Returns:
            collectiontranslatedlist
        """
        collections = []
        collection_id = 1
        
        # translated
        theme_titles = {
            'translated': 'translated',
            'translated': 'translated', 
            'translated': 'translated',
            'translated': 'translated',
            'translated': 'translated',
            'translated': 'translatedandtranslated',
            'translated': 'translated',
            'translated': 'translatedandtranslated'
        }
        
        # translated
        theme_summaries = {
            'translated': 'translated，translateduseandtranslated。',
            'translated': 'translated、translatedandtranslated。',
            'translated': 'translatedSymptomandtranslated，translated。',
            'translated': 'fromtranslatedLanguage，translated'stranslated。',
            'translated': 'translated，translated。',
            'translated': 'translated、translatedandtranslated。',
            'translated': 'translated、translated、translatedetc.translated。',
            'translated': 'translatedandtranslated，translatedReference。'
        }
        
        for theme, clip_ids in pre_clusters.items():
            # translatedper collection'stranslated
            if len(clip_ids) > MAX_CLIPS_PER_COLLECTION:
                clip_ids = clip_ids[:MAX_CLIPS_PER_COLLECTION]
            
            collections.append({
                'id': str(collection_id),
                'collection_title': theme_titles.get(theme, theme),
                'collection_summary': theme_summaries.get(theme, f'{theme}translatedcollection'),
                'clip_ids': clip_ids
            })
            collection_id += 1
        
        return collections
    
    def _validate_collections(self, collections_data: List[Dict], clips_with_titles: List[Dict]) -> List[Dict]:
        """
        verifyAndcleancollectiontranslated
        
        Args:
            collections_data: translatedcollectiontranslated
            clips_with_titles: translated
            
        Returns:
            verifytranslated'scollectiontranslated
        """
        validated_collections = []
        
        for i, collection in enumerate(collections_data):
            try:
                # verifytranslated
                if not all(key in collection for key in ['collection_title', 'collection_summary', 'clips']):
                    logger.warning(f"collection {i} translated，skip")
                    continue
                
                # verifytranslatedlist
                clip_titles = collection['clips']
                valid_clip_ids = []
                
                for clip_title in clip_titles:
                    # translated'stranslatedID
                    for clip in clips_with_titles:
                        if (clip.get('generated_title', clip['outline']) == clip_title or 
                            clip['outline'] == clip_title):
                            valid_clip_ids.append(clip['id'])
                            break
                
                if len(valid_clip_ids) < 2:
                    logger.warning(f"collection {i} translated2 ，skip")
                    continue
                
                # translatedper collection'stranslated
                if len(valid_clip_ids) > MAX_CLIPS_PER_COLLECTION:
                    valid_clip_ids = valid_clip_ids[:MAX_CLIPS_PER_COLLECTION]
                
                validated_collection = {
                    'id': str(i + 1),
                    'collection_title': collection['collection_title'],
                    'collection_summary': collection['collection_summary'],
                    'clip_ids': valid_clip_ids
                }
                
                validated_collections.append(validated_collection)
                
            except Exception as e:
                logger.error(f"verifycollection {i} failed: {str(e)}")
                continue
        
        return validated_collections
    
    def _create_default_collections(self, clips_with_titles: List[Dict]) -> List[Dict]:
        """
        createdefaultcollection（translatedfailedtranslated）
        
        Args:
            clips_with_titles: translated
            
        Returns:
            defaultcollectiontranslated
        """
        logger.info("createdefaultcollection...")
        
        # bytranslated
        high_score = []
        medium_score = []
        
        for clip in clips_with_titles:
            score = clip.get('final_score', 0)
            if score >= 0.8:
                high_score.append(clip)
            elif score >= 0.6:
                medium_score.append(clip)
        
        collections = []
        
        # createtranslatedcollection
        if len(high_score) >= 2:
            collections.append({
                'id': '1',
                'collection_title': 'translatedSelecttranslated',
                'collection_summary': 'translated'stranslatedcollection',
                'clip_ids': [clip['id'] for clip in high_score[:MAX_CLIPS_PER_COLLECTION]]
            })
        
        # createtranslatedetc.translatedcollection
        if len(medium_score) >= 2:
            collections.append({
                'id': '2',
                'collection_title': 'translatedrecommend',
                'collection_summary': 'translatedSelecttranslated',
                'clip_ids': [clip['id'] for clip in medium_score[:MAX_CLIPS_PER_COLLECTION]]
            })
        
        return collections
    
    def save_collections(self, collections_data: List[Dict], output_path: Optional[Path] = None) -> Path:
        """
        translatedcollectiontranslated
        
        Args:
            collections_data: collectiontranslated
            output_path: translatedpath
            
        Returns:
            translated'sfile path
        """
        if output_path is None:
            output_path = self.metadata_dir / "collections.json"
        
        # ensuredirectorytranslatedin
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # translated
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(collections_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"collectiontranslated: {output_path}")
        return output_path
    
    def load_collections(self, input_path: Path) -> List[Dict]:
        """
        fromfiletranslatedcollectiontranslated
        
        Args:
            input_path: translatedfile path
            
        Returns:
            collectiontranslated
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def run_step5_clustering(clips_with_titles_path: Path, output_path: Optional[Path] = None, metadata_dir: Optional[str] = None, prompt_files: Dict = None) -> List[Dict]:
    """
    translatedStep 5: translated
    
    Args:
        clips_with_titles_path: translated'stranslatedfile path
        output_path: translatedfile path
        prompt_files: translatedfile
        
    Returns:
        collectiontranslated
    """
    # translated
    with open(clips_with_titles_path, 'r', encoding='utf-8') as f:
        clips_with_titles = json.load(f)
    
    # createtranslated
    if metadata_dir is None:
        metadata_dir = METADATA_DIR
    clusterer = ClusteringEngine(metadata_dir=Path(metadata_dir), prompt_files=prompt_files)
    
    # translated
    collections_data = clusterer.cluster_clips(clips_with_titles)
    
    # translated
    if output_path is None:
        if metadata_dir is None:
            metadata_dir = METADATA_DIR
        output_path = Path(metadata_dir) / "step5_collections.json"
    
    clusterer.save_collections(collections_data, output_path)
    
    return collections_data