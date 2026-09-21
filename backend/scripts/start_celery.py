#!/usr/bin/env python3
"""
CelerystartEN
startCelery WorkerENBeatEN
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# ENprojectENdirectoryENPythonpath
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
        print(f"✅ Celery WorkerENstart (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ startCelery Workerfailed: {e}")
        return None

def start_celery_beat():
    """startCelery BeatEN"""
    print("⏰ startCelery BeatEN...")
    
    cmd = [
        "celery", "-A", "backend.core.celery_app", "beat",
        "--loglevel=info",
        "--schedule=/tmp/celerybeat-schedule",
        "--pidfile=/tmp/celerybeat.pid"
    ]
    
    try:
        process = subprocess.Popen(cmd, cwd=str(project_root))
        print(f"✅ Celery BeatENstart (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ startCelery Beatfailed: {e}")
        return None

def start_flower():
    """startFlowerEN"""
    print("🌸 startFlowerEN...")
    
    cmd = [
        "celery", "-A", "backend.core.celery_app", "flower",
        "--port=5555",
        "--loglevel=info"
    ]
    
    try:
        process = subprocess.Popen(cmd, cwd=str(project_root))
        print(f"✅ FlowerENstart (PID: {process.pid})")
        print("🌐 FlowerEN: http://localhost:5555")
        return process
    except Exception as e:
        print(f"❌ startFlowerfailed: {e}")
        return None

def signal_handler(signum, frame):
    """ENprocessingEN"""
    print("\n🛑 ENstopEN，currentlyENservice...")
    sys.exit(0)

def main():
    """EN"""
    print("🎯 AutoClip Celery taskqueuestartEN")
    print("=" * 50)
    
    # settingsENprocessing
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # checkRedisconnect
    try:
        import redis
        r = redis.Redis.from_url('redis://localhost:6379/0')
        r.ping()
        print("✅ RedisconnectEN")
    except Exception as e:
        print(f"❌ Redisconnectfailed: {e}")
        print("pleaseENRedisservicecurrentlyrun: redis-server")
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
        print("❌ ENsucceededstartENservice")
        return
    
    print("\n🎉 allserviceENstart!")
    print("📊 servicestatus:")
    print("   - Celery Worker: processingtask")
    print("   - Celery Beat: ENtaskEN")
    print("   - Flower: taskEN (http://localhost:5555)")
    print("\nEN Ctrl+C stopallservice")
    
    try:
        # EN
        while True:
            time.sleep(1)
            # checkENrun
            for process in processes:
                if process.poll() is not None:
                    print(f"⚠️  EN {process.pid} ENlogout")
    except KeyboardInterrupt:
        print("\n🛑 currentlystopservice...")
    finally:
        # stopallEN
        for process in processes:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print(f"🛑 EN {process.pid} ENstop")

if __name__ == "__main__":
    main() 