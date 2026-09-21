"""
EN - EN，useENLLMEN
"""
import json
import logging
import os
import re
from typing import Dict, Any, List
from collections.abc import Generator

# EN
try:
    from ..core.shared_config import MODEL_NAME
except ImportError:
    # ifENfailed，EN
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from core.shared_config import MODEL_NAME

# ENLLMEN
try:
    from ..core.llm_manager import get_llm_manager
except ImportError:
    # ifENfailed，EN
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from core.llm_manager import get_llm_manager

logger = logging.getLogger(__name__)

class LLMClient:
    """LLMEN - EN"""
    
    def __init__(self):
        self.model = MODEL_NAME
        self.llm_manager = get_llm_manager()
    
    def call(self, prompt: str, input_data: Any = None) -> str:
        """
        callENAPI - useENLLMEN
        
        Args:
            prompt: hintEN
            input_data: EN
            
        Returns:
            ENresponseEN
        """
        try:
            return self.llm_manager.call(prompt, input_data)
        except Exception as e:
            logger.error(f"LLMcallfailed: {str(e)}")
            raise
    
    def call_with_retry(self, prompt: str, input_data: Any = None, max_retries: int = 3) -> str:
        """
        ENretryENAPIcall
        
        Args:
            prompt: hintEN
            input_data: EN
            max_retries: ENretryEN
            
        Returns:
            ENresponseEN
        """
        try:
            return self.llm_manager.call_with_retry(prompt, input_data, max_retries)
        except Exception as e:
            logger.error(f"LLMretrycallfailed: {str(e)}")
            raise
    
    def _preprocess_llm_response(self, response: str) -> str:
        """
        ENprocessingLLMresponse，ENJSONEN
        """
        # ENtitleEN
        lines = response.split('\n')
        json_start = -1
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('[') or stripped.startswith('{'):
                json_start = i
                break
        
        if json_start >= 0:
            response = '\n'.join(lines[json_start:])
        
        # ENJSONEN
        if '```' in response:
            # ifEN```，ENbeforeEN
            parts = response.split('```')
            if len(parts) > 1:
                response = parts[0]
        
        return response.strip()
    
    def _auto_fix_response(self, response: str) -> str:
        """
        ENresponseEN
        """
        # ENBOMEN
        response = response.lstrip('\ufeff')
        response = response.strip()
        
        # EN
        response = response.replace('"', '\"').replace('"', '\"')
        
        return response
    
    def _validate_json_structure(self, parsed_data: Any) -> bool:
        """
        validateJSONEN
        """
        try:
            if not isinstance(parsed_data, list):
                logger.error(f"responseEN，EN: {type(parsed_data)}")
                return False
            
            for i, item in enumerate(parsed_data):
                if not isinstance(item, dict):
                    logger.error(f"EN{i}EN，EN: {type(item)}")
                    return False
                    
                # checkEN（EN）
                if 'outline' in item or 'start_time' in item or 'end_time' in item:
                    required_fields = ['outline', 'start_time', 'end_time']
                    for field in required_fields:
                        if field not in item:
                            logger.error(f"EN{i}EN: {field}")
                            return False
        except Exception as e:
            logger.error(f"validateJSONEN: {e}")
            return False
        
        return True
    
    def parse_json_response(self, response: str) -> Any:
        """
        ENmayENMarkdownENparseJSONEN。
        EN：
        1. ENprocessingresponse，ENJSONEN
        2. ENMarkdownEN。
        3. iffailed，thenENparseENresponse（EN）。
        4. ifENfailed，thenuseENthenENparseJSON。
        5. ENJSONerrorENparse。
        """
        
        def sanitize_string(s: str) -> str:
            """EN，ENmayENJSONparsefailedEN"""
            # ENBOMEN
            s = s.lstrip('\ufeff')
            # EN
            s = s.strip()
            # ENmayEN（EN）
            s = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)
            return s
        
        def fix_common_json_errors(json_str: str) -> str:
            """ENJSONENerror"""
            # EN
            original_str = json_str
            
            # 1. EN
            json_str = re.sub(r'}\s*{', '},{', json_str)
            json_str = re.sub(r']\s*\[', '],[', json_str)
            
            # 2. EN（EN）
            json_str = re.sub(r'}\s*\n\s*{', '},\n{', json_str)
            
            # 3. EN
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            
            # 4. EN
            json_str = re.sub(r"'([^']*?)'\s*:", r'"\1":', json_str)
            json_str = re.sub(r":\s*'([^']*?)'", r': "\1"', json_str)
            
            # 5. EN
            json_str = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', json_str)
            
            # 6. ENmayEN
            json_str = re.sub(r'\n\s*\n', '\n', json_str)
            
            # 7. EN
            # EN
            open_braces = json_str.count('{')
            close_braces = json_str.count('}')
            open_brackets = json_str.count('[')
            close_brackets = json_str.count(']')
            
            # ifEN，EN
            if open_braces > close_braces:
                json_str += '}' * (open_braces - close_braces)
            if open_brackets > close_brackets:
                json_str += ']' * (open_brackets - close_brackets)
            
            # EN
            if json_str != original_str:
                logger.debug(f"JSONEN: {original_str[:100]}...")
                logger.debug(f"JSONEN: {json_str[:100]}...")
            
            return json_str

        response = response.strip()
        
        # 0. ENprocessingresponse，ENJSONEN
        response = self._preprocess_llm_response(response)
        logger.debug(f"ENprocessingENresponse: {response[:200]}...")
        
        # 1. ENMarkdownEN
        match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response, re.DOTALL)
        if match:
            json_str = sanitize_string(match.group(1))
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                # ENerrorEN
                error_pos = e.pos if hasattr(e, 'pos') else 0
                context_start = max(0, error_pos - 50)
                context_end = min(len(json_str), error_pos + 50)
                context = json_str[context_start:context_end]
                logger.error(f"JSONparsefailedEN{error_pos}，EN: ...{context}...")
                logger.warning(f"ENMarkdownENparsefailed: {e}。ENparse。")
                
                # ENerrorENparse
                try:
                    fixed_json = fix_common_json_errors(json_str)
                    return json.loads(fixed_json)
                except json.JSONDecodeError:
                    logger.warning("ENparsefailed，ENparseENresponse。")
        
        # 2. ifENMarkdown，ENMarkdownparsefailed，ENresponse
        try:
            sanitized_response = sanitize_string(response)
            return json.loads(sanitized_response)
        except json.JSONDecodeError:
            # 3. ifENresponseENparseENfailed，EN，ENthenEN
            logger.warning("ENparseresponsefailed，ENuseENthenENJSON...")
            json_match = re.search(r'\[[\s\S]*\]|\{[\s\S]*\}', response, re.DOTALL)
            if json_match:
                json_str = sanitize_string(json_match.group())
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    # 4. ENerror
                    try:
                        fixed_json = fix_common_json_errors(json_str)
                        return json.loads(fixed_json)
                    except json.JSONDecodeError as final_e:
                        logger.error(f"ENparsefailed: {final_e}")
                        # saveENresponseEN
                        import tempfile
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                            f.write(response)
                            logger.error(f"ENresponseENsaveEN {f.name} EN")
                        raise ValueError(f"cannotENresponseENparseENJSON: {response[:200]}...") from final_e
            
            # ifENthenEN，ENfailed
            raise ValueError(f"cannotENresponseENparseENJSON: {response[:200]}...")
    
    def get_current_provider_info(self) -> Dict[str, Any]:
        """fetchcurrentEN"""
        return self.llm_manager.get_current_provider_info()