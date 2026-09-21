"""
Pipelinetranslatedconfigfile
"""

import os
from pathlib import Path

# fetchprojecttranslateddirectory
PROJECT_ROOT = Path(__file__).parent.parent.parent
BACKtranslatedD_ROOT = Path(__file__).parent.parent

# translateddirectory
DATA_DIR = PROJECT_ROOT / "data"
METADATA_DIR = DATA_DIR / "output" / "metadata"

# translatedfile path
PROMPT_DIR = PROJECT_ROOT / "prompt"
PROMPT_FILES = {
    'outline': PROMPT_DIR / "translated.txt",
    'timeline': PROMPT_DIR / "translated.txt", 
    'scoring': PROMPT_DIR / "recommendtranslated.txt",
    'recommendation': PROMPT_DIR / "recommendtranslated.txt",  # addtranslated
    'title': PROMPT_DIR / "translated.txt",
    'clustering': PROMPT_DIR / "translated.txt"
}

# ensuredirectorytranslatedin
METADATA_DIR.mkdir(parents=True, exist_ok=True)
PROMPT_DIR.mkdir(parents=True, exist_ok=True)

# APIkeyconfig
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
OPtranslatedAI_API_KEY = os.getenv('OPtranslatedAI_API_KEY')

# defaultAPIkey
DEFAULT_API_KEY = DASHSCOPE_API_KEY or OPtranslatedAI_API_KEY

# translated
MIN_SCORE_THRESHOLD = 7.0

# translatedconfig
MAX_CLIPS_PER_COLLECTION = 10
