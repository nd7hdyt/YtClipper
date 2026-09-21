#!/usr/bin/env python3
"""
Celerystarttranslated
startCelery WorkerAndBeattranslated
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# addprojecttranslateddirectorytranslatedPythonpath
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def start_celery_worker():
    """startCelery Worker"""
    print("🚀 startCelery Worker...")
    
    cmd = [
        "celery", "-A", "backend.core.celery_app", "worker",
        "--loglevel=info",
        "--concurrency=2",
        "--queues=processing,video,notification,maintenance",
        "--hostname=worker1@%h"
    ]
    
    try:
        process = subprocess.Popen(cmd, cwd=str(project_root))
        print(f"✅ Celery Workertranslatedstart (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ startCelery Workerfailed: {e}")
        return None

def start_celery_beat():
    """startCelery Beattranslated"""
    print("⏰ startCelery Beattranslated...")
    
    cmd = [
        "celery", "-A", "backend.core.celery_app", "beat",
        "--loglevel=info",
        "--schedule=/tmp/celerybeat-schedule",
        "--pidfile=/tmp/celerybeat.pid"
    ]
    
    try:
        process = subprocess.Popen(cmd, cwd=str(project_root))
        print(f"✅ Celery Beattranslatedstart (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ startCelery Beatfailed: {e}")
        return None

def start_flower():
    """startFlowermonitorInterface"""
    print("🌸 startFlowermonitorInterface...")
    
    cmd = [
        "celery", "-A", "backend.core.celery_app", "flower",
        "--port=5555",
        "--loglevel=info"
    ]
    
    try:
        process = subprocess.Popen(cmd, cwd=str(project_root))
        print(f"✅ Flowertranslatedstart (PID: {process.pid})")
        print("🌐 FlowermonitorInterface: http://localhost:5555")
        return process
    except Exception as e:
        print(f"❌ startFlowerfailed: {e}")
        return None

def signal_handler(signum, frame):
    """translatedprocesstranslated"""
    print("\n🛑 translated，translatedintranslatedservice...")
    sys.exit(0)

def main():
    """translated"""
    print("🎯 AutoClip Celery Task Queuestarttranslated")
    print("=" * 50)
    
    # settingstranslatedprocess
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # checkRedisconnect
    try:
        import redis
        r = redis.Redis.from_url('redis://localhost:6379/0')
        r.ping()
        print("✅ Redisconnecttranslated")
    except Exception as e:
        print(f"❌ Redisconnectfailed: {e}")
        print("translatedensureRedisservicetranslatedintranslated: redis-server")
        return
    
    # startservice
    processes = []
    
    # startWorker
    worker_process = start_celery_worker()
    if worker_process:
        processes.append(worker_process)
    
    # startBeat
    beat_process = start_celery_beat()
    if beat_process:
        processes.append(beat_process)
    
    # startFlower
    flower_process = start_flower()
    if flower_process:
        processes.append(flower_process)
    
    if not processes:
        print("❌ translatedsucceededstarttranslatedservice")
        return
    
    print("\n🎉 translatedservicetranslatedstart!")
    print("📊 servicestatus:")
    print("   - Celery Worker: processtask")
    print("   - Celery Beat: translatedtasktranslated")
    print("   - Flower: taskmonitorInterface (http://localhost:5555)")
    print("\nby Ctrl+C translatedservice")
    
    try:
        # etc.translatedprocess
        while True:
            time.sleep(1)
            # checkprocessIstranslatedintranslated
            for process in processes:
                if process.poll() is not None:
                    print(f"⚠️  process {process.pid} translated")
    except KeyboardInterrupt:
        print("\n🛑 translatedintranslatedservice...")
    finally:
        # translatedprocess
        for process in processes:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print(f"🛑 process {process.pid} translated")

if __name__ == "__main__":
    main() 