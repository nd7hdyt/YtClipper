"""
Step 5: Topic clustering - group similar clips into collections
"""
import json
import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import dependencies
from ..utils.llm_client import LLMClient
from ..core.shared_config import PROMPT_FILES, METADATA_DIR, MAX_CLIPS_PER_COLLECTION

logger = logging.getLogger(__name__)

class ClusteringEngine:
    """Topic clustering engine"""
    
    def __init__(self, metadata_dir: Optional[Path] = None, prompt_files: Dict = None):
        self.llm_client = LLMClient()
        
        # Load the prompt
        prompt_files_to_use = prompt_files if prompt_files is not None else PROMPT_FILES
        with open(prompt_files_to_use['clustering'], 'r', encoding='utf-8') as f:
            self.clustering_prompt = f.read()
        
        # Use the provided metadata_dir or the default
        if metadata_dir is None:
            metadata_dir = METADATA_DIR
        self.metadata_dir = metadata_dir
    
    def cluster_clips(self, clips_with_titles: List[Dict]) -> List[Dict]:
        """
        Cluster clips by topic
        
        Args:
            clips_with_titles: list of clips with titles
            
        Returns:
            list of collection data
        """
        logger.info("Starting topic clustering...")
        
        # Prepare the clustering data
        clips_for_clustering = []
        for clip in clips_with_titles:
            clips_for_clustering.append({
                'id': clip['id'],
                'title': clip.get('generated_title', clip['outline']),
                'summary': clip.get('recommend_reason', ''),
                'score': clip.get('final_score', 0)
            })
        
        # First run keyword-based pre-clustering
        pre_clusters = self._pre_cluster_by_keywords(clips_for_clustering)
        
        # Build the full prompt
        full_prompt = self.clustering_prompt + "\n\nHere is the list of video clips:\n"
        for i, clip in enumerate(clips_for_clustering, 1):
            full_prompt += f"{i}. Title: {clip['title']}\n   Summary: {clip['summary']}\n   Score: {clip['score']:.2f}\n\n"
        
        # Add the pre-clustering result as a reference
        if pre_clusters:
            full_prompt += "\n\nKeyword-based pre-clustering result (reference only):\n"
            for theme, clip_ids in pre_clusters.items():
                full_prompt += f"{theme}: {', '.join(clip_ids)}\n"
        
        try:
            # Call the LLM for clustering
            response = self.llm_client.call_with_retry(full_prompt)
            
            # Parse the JSON response
            collections_data = self.llm_client.parse_json_response(response)
            
            # Validate and clean up the collection data
            validated_collections = self._validate_collections(collections_data, clips_with_titles)
            
            # Fall back to the pre-clustering result if the LLM result is poor
            if len(validated_collections) < 3:
                logger.warning("LLM clustering result is poor, using the pre-clustering result")
                validated_collections = self._create_collections_from_pre_clusters(pre_clusters, clips_with_titles)
            
            logger.info(f"Topic clustering done, {len(validated_collections)} collections total")
            return validated_collections
            
        except Exception as e:
            logger.error(f"Topic clustering failed: {str(e)}")
            # Use the pre-clustering result as a fallback
            if pre_clusters:
                logger.info("Using the pre-clustering result as a fallback")
                return self._create_collections_from_pre_clusters(pre_clusters, clips_with_titles)
            # Return default clustering results
            return self._create_default_collections(clips_with_titles)
    
    def _pre_cluster_by_keywords(self, clips: List[Dict]) -> Dict[str, List[str]]:
        """
        Pre-cluster by keywords
        
        Args:
            clips: list of clips
            
        Returns:
            pre-clustering result
        """
        # Topic keywords (kept in Chinese: they are matched against Chinese
        # transcripts, so translating them would break pre-clustering)
        theme_keywords = {
            'EN': ['EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'AEN', 'EN', 'EN', 'EN'],
            'EN': ['EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN'],
            'EN': ['EN', 'EN', 'EN', 'EN', 'EN', 'category', 'EN', 'EN', 'EN', 'EN'],
            'EN': ['EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN'],
            'EN': ['EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'PK', 'EN'],
            'EN': ['EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN'],
            'EN': ['EN', 'EN', 'EN', 'EN', 'EN', 'EN', 'EN'],
            'EN': ['EN', 'EN', 'BEN', 'EN', 'EN', 'EN', 'EN', 'EN']
        }
        
        pre_clusters = {theme: [] for theme in theme_keywords.keys()}
        
        for clip in clips:
            # Match keywords against the combined title + summary
            text = f"{clip['title']} {clip['summary']}".lower()
            
            # Score each theme by keyword hits
            theme_scores = {}
            for theme, keywords in theme_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text)
                if score > 0:
                    theme_scores[theme] = score
            
            # Pick the highest-scoring theme
            if theme_scores:
                best_theme = max(theme_scores.keys(), key=lambda k: theme_scores[k])
                pre_clusters[best_theme].append(clip['id'])
        
        # Drop empty themes
        return {theme: clip_ids for theme, clip_ids in pre_clusters.items() if len(clip_ids) >= 2}
    
    def _create_collections_from_pre_clusters(self, pre_clusters: Dict[str, List[str]], clips_with_titles: List[Dict]) -> List[Dict]:
        """
        Build collections from the pre-clustering result
        
        Args:
            pre_clusters: pre-clustering result
            clips_with_titles: clip data
            
        Returns:
            collection data list
        """
        collections = []
        collection_id = 1
        
        # Theme title mapping
        theme_titles = {
            'EN': 'Investing & Money Insights',
            'EN': 'Career Growth Stories',
            'EN': 'Society Watch Notes',
            'EN': 'Culture Clash Tales',
            'EN': 'Livestream Moments',
            'EN': 'Relationships & Emotion',
            'EN': 'Healthy Living',
            'EN': 'Creation & Platform Life'
        }
        
        # Theme summary mapping
        theme_summaries = {
            'EN': 'Everyday cases that teach investing ideas, practical and relatable.',
            'EN': 'Career growth, skill building, and changing work mindsets.',
            'EN': 'Clear-eyed takes on social phenomena and online chaos.',
            'EN': 'Fun cross-cultural views, from food to language.',
            'EN': 'Real livestream-room moments showing the host thinking on their feet.',
            'EN': 'Dating psychology, social puzzles, and emotional resonance.',
            'EN': 'Exercise, diet, and mindset tips for staying healthy.',
            'EN': 'Creator struggles and platform mechanics, for creators.'
        }
        
        for theme, clip_ids in pre_clusters.items():
            # Cap the number of clips per collection
            if len(clip_ids) > MAX_CLIPS_PER_COLLECTION:
                clip_ids = clip_ids[:MAX_CLIPS_PER_COLLECTION]
            
            collections.append({
                'id': str(collection_id),
                'collection_title': theme_titles.get(theme, theme),
                'collection_summary': theme_summaries.get(theme, f'Best moments about {theme}'),
                'clip_ids': clip_ids
            })
            collection_id += 1
        
        return collections
    
    def _validate_collections(self, collections_data: List[Dict], clips_with_titles: List[Dict]) -> List[Dict]:
        """
        Validate and clean up the collection data
        
        Args:
            collections_data: raw collection data
            clips_with_titles: clip data
            
        Returns:
            validated collection data
        """
        validated_collections = []
        
        for i, collection in enumerate(collections_data):
            try:
                # Check required fields
                if not all(key in collection for key in ['collection_title', 'collection_summary', 'clips']):
                    logger.warning(f"Collection {i} is missing required fields, skipping")
                    continue
                
                # Validate the clip list
                clip_titles = collection['clips']
                valid_clip_ids = []
                
                for clip_title in clip_titles:
                    # Find the matching clip ID by title
                    for clip in clips_with_titles:
                        if (clip.get('generated_title', clip['outline']) == clip_title or 
                            clip['outline'] == clip_title):
                            valid_clip_ids.append(clip['id'])
                            break
                
                if len(valid_clip_ids) < 2:
                    logger.warning(f"Collection {i} has fewer than 2 valid clips, skipping")
                    continue
                
                # Cap the number of clips per collection
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
                logger.error(f"Failed to validate collection {i}: {str(e)}")
                continue
        
        return validated_collections
    
    def _create_default_collections(self, clips_with_titles: List[Dict]) -> List[Dict]:
        """
        Create default collections (when clustering fails)
        
        Args:
            clips_with_titles: clip data
            
        Returns:
            default collection data
        """
        logger.info("Creating default collections...")
        
        # Group by score
        high_score = []
        medium_score = []
        
        for clip in clips_with_titles:
            score = clip.get('final_score', 0)
            if score >= 0.8:
                high_score.append(clip)
            elif score >= 0.6:
                medium_score.append(clip)
        
        collections = []
        
        # High-score collection
        if len(high_score) >= 2:
            collections.append({
                'id': '1',
                'collection_title': 'Top-Rated Clip Picks',
                'collection_summary': 'A collection of the highest-scoring highlights',
                'clip_ids': [clip['id'] for clip in high_score[:MAX_CLIPS_PER_COLLECTION]]
            })
        
        # Medium-score collection
        if len(medium_score) >= 2:
            collections.append({
                'id': '2',
                'collection_title': 'Recommended Quality Clips',
                'collection_summary': 'Hand-picked quality clips',
                'clip_ids': [clip['id'] for clip in medium_score[:MAX_CLIPS_PER_COLLECTION]]
            })
        
        return collections
    
    def save_collections(self, collections_data: List[Dict], output_path: Optional[Path] = None) -> Path:
        """
        Save the collection data
        
        Args:
            collections_data: collection data
            output_path: output path
            
        Returns:
            path of the saved file
        """
        if output_path is None:
            output_path = self.metadata_dir / "collections.json"
        
        # Make sure the directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the data
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(collections_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Collection data saved to: {output_path}")
        return output_path
    
    def load_collections(self, input_path: Path) -> List[Dict]:
        """
        Load collection data from a file
        
        Args:
            input_path: input file path
            
        Returns:
            collection data
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def run_step5_clustering(clips_with_titles_path: Path, output_path: Optional[Path] = None, metadata_dir: Optional[str] = None, prompt_files: Dict = None) -> List[Dict]:
    """
    Run Step 5: topic clustering
    
    Args:
        clips_with_titles_path: path to the titled-clips file
        output_path: output file path
        prompt_files: custom prompt files
        
    Returns:
        collection data
    """
    # Load the data
    with open(clips_with_titles_path, 'r', encoding='utf-8') as f:
        clips_with_titles = json.load(f)
    
    # Create the clusterer
    if metadata_dir is None:
        metadata_dir = METADATA_DIR
    clusterer = ClusteringEngine(metadata_dir=Path(metadata_dir), prompt_files=prompt_files)
    
    # Run clustering
    collections_data = clusterer.cluster_clips(clips_with_titles)
    
    # Save the result
    if output_path is None:
        if metadata_dir is None:
            metadata_dir = METADATA_DIR
        output_path = Path(metadata_dir) / "step5_collections.json"
    
    clusterer.save_collections(collections_data, output_path)
    
    return collections_data