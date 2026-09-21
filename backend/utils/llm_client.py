"""
translatedmodeltranslated - translatedPackagetranslated，usetranslated'sLLMtranslated
"""
import json
import logging
import os
import re
from typing import Dict, Any, List
from collections.abc import Generator

# fixedimportissue
try:
    from ..core.shared_config import MODEL_NAME
except ImportError:
    # iftranslatedimportfailed，translatedimport
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from core.shared_config import MODEL_NAME

# importtranslated'sLLMtranslated
try:
    from ..core.llm_manager import get_llm_manager
except ImportError:
    # iftranslatedimportfailed，translatedimport
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from core.llm_manager import get_llm_manager

logger = logging.getLogger(__name__)

class LLMClient:
    """LLMtranslated - translatedPackagetranslated"""
    
    def __init__(self):
        self.model = MODEL_NAME
        self.llm_manager = get_llm_manager()
    
    def call(self, prompt: str, input_data: Any = None) -> str:
        """
        calltranslatedmodelAPI - usetranslated'sLLMtranslated
        
        Args:
            prompt: translated
            input_data: translated
            
        Returns:
            modeltranslated
        """
        try:
            return self.llm_manager.call(prompt, input_data)
        except Exception as e:
            logger.error(f"LLMcallfailed: {str(e)}")
            raise
    
    def call_with_retry(self, prompt: str, input_data: Any = None, max_retries: int = 3) -> str:
        """
        translated'sAPIcall
        
        Args:
            prompt: translated
            input_data: translated
            max_retries: translated
            
        Returns:
            modeltranslated
        """
        try:
            return self.llm_manager.call_with_retry(prompt, input_data, max_retries)
        except Exception as e:
            logger.error(f"LLMtranslatedcallfailed: {str(e)}")
            raise
    
    def _preprocess_llm_response(self, response: str) -> str:
        """
        translatedprocessLLMtranslated，translated'stranslatedJSONtranslated
        """
        # translated'stranslatedAndtranslated
        lines = response.split('\n')
        json_start = -1
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('[') or stripped.startswith('{'):
                json_start = i
                break
        
        if json_start >= 0:
            response = '\n'.join(lines[json_start:])
        
        # translated'stranslatedJSONtranslated
        if '```' in response:
            # iftranslatedmulti ```，translatedNo.one translated'stranslated
            parts = response.split('```')
            if len(parts) > 1:
                response = parts[0]
        
        return response.strip()
    
    def _auto_fix_response(self, response: str) -> str:
        """
        translatedfixedtranslated'stranslatedissue
        """
        # translatedBOMAndtranslated
        response = response.lstrip('\ufeff')
        response = response.strip()
        
        # fixedtranslated
        response = response.replace('"', '\"').replace('"', '\"')
        
        return response
    
    def _validate_json_structure(self, parsed_data: Any) -> bool:
        """
        verifyJSONtranslated'stranslated
        """
        try:
            if not isinstance(parsed_data, list):
                logger.error(f"translatedIstranslatedformat，translated: {type(parsed_data)}")
                return False
            
            for i, item in enumerate(parsed_data):
                if not isinstance(item, dict):
                    logger.error(f"No.{i} translatedIstranslatedformat，translated: {type(item)}")
                    return False
                    
                # checktranslated（cantranslated）
                if 'outline' in item or 'start_time' in item or 'end_time' in item:
                    required_fields = ['outline', 'start_time', 'end_time']
                    for field in required_fields:
                        if field not in item:
                            logger.error(f"No.{i} translated: {field}")
                            return False
        except Exception as e:
            logger.error(f"verifyJSONtranslated: {e}")
            return False
        
        return True
    
    def parse_json_response(self, response: str) -> Any:
        """
        fromcantranslatedPackageincludeMarkdownformat'stranslatedJSONtranslated。
        translatedmultitranslated：
        1. translatedprocesstranslated，translatedJSONtranslated
        2. translatedfromMarkdowntranslated。
        3. iftranslatedfailed，translated translated（intranslated）。
        4. iftranslatedfailed，translatedusetranslatedusetranslatedJSON。
        5. translatedfixedtranslatedJSONerrortranslated。
        """
        
        def sanitize_string(s: str) -> str:
            """translated'stranslated，translatedcantranslatedJSONtranslatedfailed'stranslated"""
            # translatedBOMtranslated
            s = s.lstrip('\ufeff')
            # translated
            s = s.strip()
            # translatedcantranslated'stranslated（translated'stranslatedAndtranslated）
            s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)
            return s
        
        def fix_common_json_errors(json_str: str) -> str:
            """fixedtranslated'sJSONformaterror"""
            # translatedusetranslated
            original_str = json_str
            
            # 1. fixedtranslated'sissue
            json_str = re.sub(r'}\s*{', '},{', json_str)
            json_str = re.sub(r']\s*\[', '],[', json_str)
            
            # 2. fixedtranslated'sissue（translated'stranslated）
            json_str = re.sub(r'}\s*\n\s*{', '},\n{', json_str)
            
            # 3. fixedmultitranslated'stranslated
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            
            # 4. fixedtranslated
            json_str = re.sub(r"'([^']*?)'\s*:", r'"\1":', json_str)
            json_str = re.sub(r":\s*'([^']*?)'", r': "\1"', json_str)
            
            # 5. fixedtranslated'sissue
            json_str = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', json_str)
            
            # 6. fixedcantranslated'stranslatedissue
            json_str = re.sub(r'\n\s*\n', '\n', json_str)
            
            # 7. ensuretranslatedAndtranslated'stranslated
            # translatedAndtranslated'stranslated
            open_braces = json_str.count('{')
            close_braces = json_str.count('}')
            open_brackets = json_str.count('[')
            close_brackets = json_str.count(']')
            
            # iftranslated，translatedfixed
            if open_braces > close_braces:
                json_str += '}' * (open_braces - close_braces)
            if open_brackets > close_brackets:
                json_str += ']' * (open_brackets - close_brackets)
            
            # translatedfixedtranslated
            if json_str != original_str:
                logger.debug(f"JSONfixedtranslated: {original_str[:100]}...")
                logger.debug(f"JSONfixedtranslated: {json_str[:100]}...")
            
            return json_str

        response = response.strip()
        
        # 0. translatedprocesstranslated，translatedJSONtranslated
        response = self._preprocess_llm_response(response)
        logger.debug(f"translatedprocesstranslated'stranslated: {response[:200]}...")
        
        # 1. translatedfromMarkdowntranslated
        match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response, re.DOTALL)
        if match:
            json_str = sanitize_string(match.group(1))
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                # translated'serrortranslatedAndtranslated
                error_pos = e.pos if hasattr(e, 'pos') else 0
                context_start = max(0, error_pos - 50)
                context_end = min(len(json_str), error_pos + 50)
                context = json_str[context_start:context_end]
                logger.error(f"JSONtranslatedfailedintranslated{error_pos}，translated: ...{context}...")
                logger.warning(f"fromMarkdowntranslated'stranslatedfailed: {e}。translatedfixedtranslated。")
                
                # translatedfixedtranslatederrortranslated
                try:
                    fixed_json = fix_common_json_errors(json_str)
                    return json.loads(fixed_json)
                except json.JSONDecodeError:
                    logger.warning("fixedtranslatedfailed，translated translated。")
        
        # 2. iftranslatedMarkdown，orMarkdowntranslatedfailed，translated translated
        try:
            sanitized_response = sanitize_string(response)
            return json.loads(sanitized_response)
        except json.JSONDecodeError:
            # 3. iftranslated translatedfailed，translatedonetranslated，usetranslatedusetranslated
            logger.warning("translatedfailed，translatedusetranslatedusetranslatedJSON...")
            json_match = re.search(r'\[[\s\S]*\]|\{[\s\S]*\}', response, re.DOTALL)
            if json_match:
                json_str = sanitize_string(json_match.group())
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    # 4. translatedfixedtranslatederror
                    try:
                        fixed_json = fix_common_json_errors(json_str)
                        return json.loads(fixed_json)
                    except json.JSONDecodeError as final_e:
                        logger.error(f"translatedfailed: {final_e}")
                        # translated
                        import tempfile
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                            f.write(response)
                            logger.error(f"translated {f.name} translated")
                        raise ValueError(f"translatedfromtranslated'sJSON: {response[:200]}...") from final_e
            
            # iftranslatedusetranslated，translatedfailed
            raise ValueError(f"translatedfromtranslated'sJSON: {response[:200]}...")
    
    def get_current_provider_info(self) -> Dict[str, Any]:
        """fetchtranslatedProvidesproviderinfo"""
        return self.llm_manager.get_current_provider_info()