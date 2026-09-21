# AutoClip start

## 📋 overview

AutoClip based onAIclip，backend。start。

## 🚀 quick start

### 1. start（recommend）

```bash
# start（checkmonitor）
./start_autoclip.sh

# start（dev environment，check）
./quick_start.sh
```

### 2. 

```bash
# checkstatus
./status_autoclip.sh

# service
./stop_autoclip.sh
```

## 📊 

### backendservice
- **FastAPI**: RESTful API  WebSocket support
- **Celery**: 
- **Redis**: proxycache
- **SQLite**: 

### frontendservice
- **React**: 
- **Vite**: server
- **TypeScript**: security

## 🔧 

### 
- macOS  Linux
- Python 3.8+
- Node.js 16+
- Redis server

### dependenciesinstall

```bash
# 1. create
python3 -m venv venv
source venv/bin/activate

# 2. installPythondependencies
pip install -r requirements.txt

# 3. installfrontenddependencies
cd frontend
npm install
cd ..

# 4. installRedis（macOS）
brew install redis
brew services start redis

# 5. configenv var
cp env.example .env
# edit .env file，config
```

## 📝 configfile

### env var (.env)

```bash
# databaseconfig
DATABASE_URL=sqlite:///./data/autoclip.db

# Redisconfig
REDIS_URL=redis://localhost:6379/0

# APIconfig
API_DASHSCOPE_API_KEY=your_api_key_here
API_MODEL_NAME=qwen-plus

# config
LOG_LEVEL=INFO
ENVIRONMENT=development
DEBUG=true
```

## 🌐 serviceport

| service | port |  |
|------|------|------|
| frontend | 3000 | React server |
| backendAPI | 8000 | FastAPI server |
| Redis | 6379 | proxy |
| APIdocs | 8000/docs | Swagger UI |

## 📁 

```
autoclip/
├── backend/                 # backend
│   ├── api/                # APIroute
│   ├── core/               # config
│   ├── models/             # model
│   ├── services/           # 
│   └── tasks/              # Celery
├── frontend/               # frontend
│   ├── src/                # 
│   └── public/             # 
├── data/                   # 
│   ├── projects/           # project
│   └── uploads/            # upload file
├── logs/                   # file
├── scripts/                # tool
└── *.sh                    # start
```

## 🔍 troubleshooting

### FAQ

1. **port**
   ```bash
   # checkport
   lsof -i :8000
   lsof -i :3000
   
   # 
   kill -9 <PID>
   ```

2. **Redisconnection failed**
   ```bash
   # checkRedisstatus
   redis-cli ping
   
   # startRedis
   brew services start redis  # macOS
   systemctl start redis      # Linux
   ```

3. **Pythondependenciesissue**
   ```bash
   # installdependencies
   pip install -r requirements.txt --force-reinstall
   ```

4. **frontenddependenciesissue**
   ```bash
   # install
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

### view

```bash
# view
tail -f logs/*.log

# viewservice
tail -f logs/backend.log
tail -f logs/frontend.log
tail -f logs/celery.log
```

### statuscheck

```bash
# statuscheck
./status_autoclip.sh

# checkservice
curl http://localhost:8000/api/v1/health/
curl http://localhost:3000/
redis-cli ping
```

## 🛠️ dev mode

### backend dev

```bash
# 
source venv/bin/activate

# settingsPython
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# startbackend（dev mode）
python -m uvicorn backend.main:app --reload --port 8000
```

### frontend dev

```bash
# frontend
cd frontend

# startserver
npm run dev
```

### Celery Worker

```bash
# startWorker（ -Q： celery_app.task_routes route，
#  -Q  worker default `celery` ， `processing` ）
celery -A backend.core.celery_app worker --loglevel=info -Q celery,processing,video,notification,upload

# startBeat
celery -A backend.core.celery_app beat --loglevel=info

# startFlowermonitor
celery -A backend.core.celery_app flower --port=5555
```

## 📈 performance

### productionconfig

1. **database**
   - usePostgreSQLSQLite
   - config
   - cache

2. **Redis**
   - configmemorylimit
   - 
   - settings

3. **Celery**
   - 
   - configroute
   - backend

## 🔒 securityconfig

### productionsecurity

1. **env var**
   - use
   - key
   - limitAPIaccess

2. **security**
   - config
   - useHTTPS
   - limitCORS

3. **security**
   - 
   - 
   - access

## 📞 support

if you encounter issues，：

1. viewfile
2. statuscheck
3. checkconfig
4. troubleshooting

## 📄 

project MIT 。
