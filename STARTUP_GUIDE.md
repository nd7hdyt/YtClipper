# AutoClip EN

## 📋 EN

AutoClip ENBased onAIENProcessing System，AdoptsFrontend-Backend SeparationEN。EN。

## 🚀 Quick Start

### 1. One-Click Start（EN）

```bash
# EN（EN）
./start_autoclip.sh

# EN（EN，EN）
./quick_start.sh
```

### 2. EN

```bash
# EN
./status_autoclip.sh

# EN
./stop_autoclip.sh
```

## 📊 System Architecture

### EN
- **FastAPI**: RESTful API EN WebSocket Support
- **Celery**: ENTask Queue
- **Redis**: EN
- **SQLite**: EN

### EN
- **React**: ENInterface
- **Vite**: EN
- **TypeScript**: EN

## 🔧 Requirements

### EN
- macOS EN Linux
- Python 3.8+
- Node.js 16+
- Redis EN

### EN

```bash
# 1. EN
python3 -m venv venv
source venv/bin/activate

# 2. ENPythonEN
pip install -r requirements.txt

# 3. EN
cd frontend
npm install
cd ..

# 4. ENRedis（macOS）
brew install redis
brew services start redis

# 5. EN
cp env.example .env
# EN .env EN，EN
```

## 📝 EN

### EN (.env)

```bash
# EN
DATABASE_URL=sqlite:///./data/autoclip.db

# RedisEN
REDIS_URL=redis://localhost:6379/0

# APIEN
API_DASHSCOPE_API_KEY=your_api_key_here
API_MODEL_NAME=qwen-plus

# EN
LOG_LEVEL=INFO
ENVIRONMENT=development
DEBUG=true
```

## 🌐 EN

| EN | EN | EN |
|------|------|------|
| ENInterface | 3000 | React EN |
| ENAPI | 8000 | FastAPI EN |
| Redis | 6379 | EN |
| APIEN | 8000/docs | Swagger UI |

## 📁 EN

```
autoclip/
├── backend/                 # EN
│   ├── api/                # APIEN
│   ├── core/               # EN
│   ├── models/             # EN
│   ├── services/           # EN
│   └── tasks/              # CeleryEN
├── frontend/               # EN
│   ├── src/                # EN
│   └── public/             # EN
├── data/                   # EN
│   ├── projects/           # EN
│   └── uploads/            # UploadEN
├── logs/                   # EN
├── scripts/                # EN
└── *.sh                    # EN
```

## 🔍 Troubleshooting

### FAQ

1. **EN**
   ```bash
   # EN
   lsof -i :8000
   lsof -i :3000
   
   # EN
   kill -9 <PID>
   ```

2. **RedisEN**
   ```bash
   # ENRedisEN
   redis-cli ping
   
   # ENRedis
   brew services start redis  # macOS
   systemctl start redis      # Linux
   ```

3. **PythonEN**
   ```bash
   # EN
   pip install -r requirements.txt --force-reinstall
   ```

4. **EN**
   ```bash
   # EN
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

### EN

```bash
# EN
tail -f logs/*.log

# EN
tail -f logs/backend.log
tail -f logs/frontend.log
tail -f logs/celery.log
```

### EN

```bash
# EN
./status_autoclip.sh

# EN
curl http://localhost:8000/api/v1/health/
curl http://localhost:3000/
redis-cli ping
```

## 🛠️ EN

### EN

```bash
# EN
source venv/bin/activate

# ENPythonEN
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# EN（EN）
python -m uvicorn backend.main:app --reload --port 8000
```

### EN

```bash
# EN
cd frontend

# EN
npm run dev
```

### Celery Worker

```bash
# ENWorker（EN -Q：EN celery_app.task_routes EN，
# EN -Q EN worker EN `celery` EN，EN `processing` EN）
celery -A backend.core.celery_app worker --loglevel=info -Q celery,processing,video,notification,upload

# ENBeatEN
celery -A backend.core.celery_app beat --loglevel=info

# ENFlowerEN
celery -A backend.core.celery_app flower --port=5555
```

## 📈 Performance

### EN

1. **EN**
   - ENPostgreSQLENSQLite
   - EN
   - EN

2. **RedisEN**
   - EN
   - EN
   - EN

3. **CeleryEN**
   - EN
   - EN
   - EN

## 🔒 Security

### EN

1. **EN**
   - EN
   - EN
   - ENAPIEN

2. **EN**
   - EN
   - ENHTTPS
   - ENCORS

3. **EN**
   - EN
   - EN
   - EN

## 📞 Support

EN，EN：

1. EN
2. EN
3. EN
4. ReferenceTroubleshootingEN

## 📄 License

ENAdopts MIT License。
