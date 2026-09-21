#!/usr/bin/env python3
"""
Whisperprocessmonitortool
usetranslatedAndtranslated'sWhisperprocess
"""

import psutil
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_whisper_processes():
    """translatedintranslated'sWhisperprocess"""
    whisper_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
        try:
            cmdline = proc.info['cmdline'] or []
            if 'whisper' in proc.info['name'].lower() or any('whisper' in str(arg).lower() for arg in cmdline):
                whisper_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': ' '.join(cmdline),
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_mb': proc.info['memory_info'].rss / 1024 / 1024
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return whisper_processes

def check_duplicate_whisper_processes():
    """checkIstranslated'sWhisperprocessprocesstranslatedone file"""
    whisper_processes = find_whisper_processes()
    
    if not whisper_processes:
        logger.info("translatedWhisperprocess")
        return True
    
    logger.info(f"translated {len(whisper_processes)}  Whisperprocess:")
    
    # byvideofiletranslated
    video_files = {}
    for proc in whisper_processes:
        cmdline = proc['cmdline']
        # translatedvideofile path
        parts = cmdline.split()
        video_file = None
        for i, part in enumerate(parts):
            if part.endswith(('.mp4', '.avi', '.mkv', '.mov', '.wav', '.mp3')):
                video_file = part
                break
        
        if video_file:
            if video_file not in video_files:
                video_files[video_file] = []
            video_files[video_file].append(proc)
    
    # checktranslatedprocess
    duplicates_found = False
    for video_file, processes in video_files.items():
        if len(processes) > 1:
            logger.warning(f"translatedprocessfile {video_file}:")
            duplicates_found = True
            for proc in processes:
                logger.warning(f"  PID {proc['pid']}: CPU {proc['cpu_percent']:.1f}%, translated {proc['memory_mb']:.1f}MB")
    
    if not duplicates_found:
        logger.info("translatedprocess'sWhisperprocess")
    
    return not duplicates_found

def kill_duplicate_whisper_processes():
    """translated'sWhisperprocess"""
    whisper_processes = find_whisper_processes()
    
    if not whisper_processes:
        logger.info("translatedWhisperprocesstranslated")
        return
    
    # byvideofiletranslated
    video_files = {}
    for proc in whisper_processes:
        cmdline = proc['cmdline']
        parts = cmdline.split()
        video_file = None
        for i, part in enumerate(parts):
            if part.endswith(('.mp4', '.avi', '.mkv', '.mov', '.wav', '.mp3')):
                video_file = part
                break
        
        if video_file:
            if video_file not in video_files:
                video_files[video_file] = []
            video_files[video_file].append(proc)
    
    # translatedCPUusetranslated'sprocess，translated's
    for video_file, processes in video_files.items():
        if len(processes) > 1:
            logger.info(f"processtranslatedprocess - file: {video_file}")
            
            # byCPUusetranslated，translated's
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            keep_process = processes[0]
            
            logger.info(f"translatedprocess PID {keep_process['pid']} (CPU: {keep_process['cpu_percent']:.1f}%)")
            
            # translatedprocess
            for proc in processes[1:]:
                try:
                    logger.info(f"translatedprocess PID {proc['pid']}")
                    psutil.Process(proc['pid']).terminate()
                except psutil.NoSuchProcess:
                    logger.info(f"process PID {proc['pid']} translatednot found")
                except psutil.AccessDenied:
                    logger.error(f"translatedprocess PID {proc['pid']} (translated)")

def main():
    """translated"""
    if len(sys.argv) > 1 and sys.argv[1] == '--kill-duplicates':
        logger.info("checktranslated'sWhisperprocess...")
        kill_duplicate_whisper_processes()
    else:
        logger.info("checkWhisperprocessstatus...")
        if check_duplicate_whisper_processes():
            logger.info("✅ Systemstatustranslated")
            sys.exit(0)
        else:
            logger.warning("⚠️ translated'sWhisperprocess")
            sys.exit(1)

if __name__ == '__main__':
    main()
