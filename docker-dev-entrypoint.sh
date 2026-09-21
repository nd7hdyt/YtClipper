#!/bin/bash

# Dockertranslatedstarttranslated
# translated，translatedfrontendviteissue

set -euo pipefail

echo "🚀 startAutoCliptranslated..."

# settingstranslated
export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

# ensuretranslateddirectorytranslatedin
mkdir -p /app/data/projects /app/data/uploads /app/data/temp /app/data/output /app/logs

# translated
source /app/venv/bin/activate

# checktranslatedinstallfrontenddependencies
echo "📦 checkfrontenddependencies..."
cd /app/frontend
if [ ! -d node_modules ] || [ ! -f node_modules/.bin/vite ]; then
    echo "installfrontenddependencies..."
    npm install
fi

# checkviteIstranslatedinstall
if [ ! -f node_modules/.bin/vite ]; then
    echo "❌ vitetranslatedinstall，translatedinstall..."
    npm install vite
fi

# returntranslateddirectory
cd /app

# startbackendservice
echo "🔧 startbackendservice..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKtranslatedD_PID=$!

# etc.translatedbackendstart
sleep 3

# startfrontendservice
echo "🌐 startfrontendservice..."
cd /app/frontend
npx vite --host 0.0.0.0 --port 3000 &
FRONTtranslatedD_PID=$!

# returntranslateddirectory
cd /app

echo "✅ servicestarttranslated"
echo "  backendAPI: http://localhost:8000"
echo "  frontendInterface: http://localhost:3000"

# etc.translatedprocess
wait