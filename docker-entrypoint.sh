#!/bin/bash

# DockerENStartScript
# ENDockerEnvironmentEN，ENConfigEN

set -euo pipefail

# ENEnvironmentEN
export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

# EN
mkdir -p /app/data/projects /app/data/uploads /app/data/temp /app/data/output /app/logs

# IfEN，EN
if [[ ! -f /app/data/autoclip.db ]]; then
    echo "EN..."
    python -c "
import sys
sys.path.insert(0, '/app')
from backend.core.database import engine, Base
from backend.models import project, task, clip, collection, bilibili
try:
    Base.metadata.create_all(bind=engine)
    print('ENSuccess')
except Exception as e:
    print(f'ENFailed: {e}')
    sys.exit(1)
"
fi

# CheckRedisEN
echo "CheckRedisEN..."
python -c "
import os
import redis
try:
    redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    r = redis.Redis.from_url(redis_url, decode_responses=True)
    r.ping()
    print(f'RedisENSuccess: {redis_url}')
except Exception as e:
    print(f'RedisENFailed: {e}')
    print('ENSQLiteEN')
"

# StartEN
echo "StartAutoClipEN..."
exec "$@"