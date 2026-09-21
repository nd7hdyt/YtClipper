#!/bin/bash

# DockerENEnvironmentStartScript
# ENEnvironmentEN，ENviteEN

set -euo pipefail

echo "🚀 StartAutoClipENEnvironment..."

# ENEnvironmentEN
export PYTHONPATH=/app
export PYTHONUNBUFFERED=1

# EN
mkdir -p /app/data/projects /app/data/uploads /app/data/temp /app/data/output /app/logs

# ENEnvironment
source /app/venv/bin/activate

# CheckENInstallENDependencies
echo "📦 CheckENDependencies..."
cd /app/frontend
if [ ! -d node_modules ] || [ ! -f node_modules/.bin/vite ]; then
    echo "InstallENDependencies..."
    npm install
fi

# CheckviteENInstall
if [ ! -f node_modules/.bin/vite ]; then
    echo "❌ viteENInstall，ENInstall..."
    npm install vite
fi

# EN
cd /app

# StartENService
echo "🔧 StartENService..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# ENStart
sleep 3

# StartENService
echo "🌐 StartENService..."
cd /app/frontend
npx vite --host 0.0.0.0 --port 3000 &
FRONTEND_PID=$!

# EN
cd /app

echo "✅ ServiceStartCompleted"
echo "  ENAPI: http://localhost:8000"
echo "  EN: http://localhost:3000"

# ENAllEN
wait