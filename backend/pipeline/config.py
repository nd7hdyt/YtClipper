"""
PipelineENconfigfile
"""

import os
from pathlib import Path

# fetchprojectENdirectory
PROJECT_ROOT = Path(__file__).parent.parent.parent
BACKEND_ROOT = Path(__file__).parent.parent

# ENdirectory
DATA_DIR = PROJECT_ROOT / "data"
METADATA_DIR = DATA_DIR / "output" / "metadata"

# hintENfilepath
PROMPT_DIR = PROJECT_ROOT / "prompt"
PROMPT_FILES = {
    'outline': PROMPT_DIR / "EN.txt",
    'timeline': PROMPT_DIR / "timeEN.txt", 
    'scoring': PROMPT_DIR / "EN.txt",
    'recommendation': PROMPT_DIR / "EN.txt",  # EN
    'title': PROMPT_DIR / "titlegenerate.txt",
    'clustering': PROMPT_DIR / "EN.txt"
}

# ENdirectoryEN
METADATA_DIR.mkdir(parents=True, exist_ok=True)
PROMPT_DIR.mkdir(parents=True, exist_ok=True)

# APIENconfig
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ENAPIEN
DEFAULT_API_KEY = DASHSCOPE_API_KEY or OPENAI_API_KEY

# scoringEN
MIN_SCORE_THRESHOLD = 7.0

# ENconfig
MAX_CLIPS_PER_COLLECTION = 10
