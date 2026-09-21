#!/bin/bash

# Dockertranslatedstarttranslated
# translatedDockertranslated，translatedAndconfigissue

set -euo pipefail

# settingstranslated
export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

# ensuretranslateddirectorytranslatedintranslated
mkdir -p /app/data/projects /app/data/uploads /app/data/temp /app/data/output /app/logs

# iftranslateddirectorytranslated，createtranslated'sfile
if [[ ! -f /app/data/autoclip.db ]]; then
    echo "translateddatabase..."
    python -c "
import sys
sys.path.insert(0, '/app')
from backend.core.database import engine, Base
from backend.models import project, task, clip, collection, bilibili
try:
    Base.metadata.create_all(bind=engine)
    print('databasetranslatedsucceeded')
except Exception as e:
    print(f'databasetranslatedfailed: {e}')
    sys.exit(1)
"
fi

# checkRedisconnect
echo "checkRedisconnect..."
python -c "
import os
import redis
try:
    redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    r = redis.Redis.from_url(redis_url, decode_responses=True)
    r.ping()
    print(f'Redisconnectsucceeded: {redis_url}')
except Exception as e:
    print(f'Redisconnectfailed: {e}')
    print('translateduseSQLitetranslatedSelecttranslated')
"

# starttranslateduse
echo "startAutoCliptranslateduse..."
exec "$@"