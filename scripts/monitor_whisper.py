#!/usr/bin/env python3
"""
WhisperENTool
ENWhisperEN
"""

import psutil
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_whisper_processes():
    """ENAllCurrentlyENWhisperEN"""
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
    """CheckENWhisperENProcessingEN"""
    whisper_processes = find_whisper_processes()
    
    if not whisper_processes:
        logger.info("ENWhisperEN")
        return True
    
    logger.info(f"EN {len(whisper_processes)} ENWhisperEN:")
    
    # EN
    video_files = {}
    for proc in whisper_processes:
        cmdline = proc['cmdline']
        # EN
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
    
    # CheckENProcessing
    duplicates_found = False
    for video_file, processes in video_files.items():
        if len(processes) > 1:
            logger.warning(f"ENProcessingEN {video_file}:")
            duplicates_found = True
            for proc in processes:
                logger.warning(f"  PID {proc['pid']}: CPU {proc['cpu_percent']:.1f}%, EN {proc['memory_mb']:.1f}MB")
    
    if not duplicates_found:
        logger.info("ENProcessingENWhisperEN")
    
    return not duplicates_found

def kill_duplicate_whisper_processes():
    """ENWhisperEN"""
    whisper_processes = find_whisper_processes()
    
    if not whisper_processes:
        logger.info("ENWhisperENNeedEN")
        return
    
    # EN
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
    
    # ENCPUEN，EN
    for video_file, processes in video_files.items():
        if len(processes) > 1:
            logger.info(f"ProcessingEN - EN: {video_file}")
            
            # ENCPUEN，EN
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            keep_process = processes[0]
            
            logger.info(f"EN PID {keep_process['pid']} (CPU: {keep_process['cpu_percent']:.1f}%)")
            
            # EN
            for proc in processes[1:]:
                try:
                    logger.info(f"EN PID {proc['pid']}")
                    psutil.Process(proc['pid']).terminate()
                except psutil.NoSuchProcess:
                    logger.info(f"EN PID {proc['pid']} AlreadyEN")
                except psutil.AccessDenied:
                    logger.error(f"EN PID {proc['pid']} (EN)")

def main():
    """EN"""
    if len(sys.argv) > 1 and sys.argv[1] == '--kill-duplicates':
        logger.info("CheckENWhisperEN...")
        kill_duplicate_whisper_processes()
    else:
        logger.info("CheckWhisperENStatus...")
        if check_duplicate_whisper_processes():
            logger.info("✅ SystemStatusEN")
            sys.exit(0)
        else:
            logger.warning("⚠️ ENWhisperEN")
            sys.exit(1)

if __name__ == '__main__':
    main()
