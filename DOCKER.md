# Docker deploy

docsuseDockerdeployAutoClip。

## 📋 

- [quick start](#quick start)
- [productiondeploy](#productiondeploy)
- [dev environmentdeploy](#dev environmentdeploy)
- [config notes](#config notes)
- [data management](#data management)
- [troubleshooting](#troubleshooting)

## 🚀 quick start

### 

- Docker 20.10+
- Docker Compose 2.0+
-  4GB availablememory
-  10GB available

### start

```bash
# project
git clone https://github.com/your-username/autoclip.git
cd autoclip

# configenv var
cp env.example .env
# edit .env file，config

# Linux ： root ，bind mount need
mkdir -p data logs uploads && chmod -R 777 data logs uploads

# startservice
docker-compose up -d

# viewservicestatus
docker-compose ps

# view
docker-compose logs -f
```

### accessservice

- **frontend**: http://localhost:3000
- **backendAPI**: http://localhost:8000
- **APIdocs**: http://localhost:8000/docs
- **Flowermonitor**: http://localhost:5555

## 🏭 productiondeploy

### useconfig

```bash
# useproductionconfig
docker-compose -f docker-compose.yml up -d

# 
docker-compose up -d

# viewservicestatus
docker-compose ps

# view
docker-compose logs -f autoclip
```

### production

1. **limit**
```yaml
# docker-compose.ymllimit
services:
  autoclip:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

2. ****
```bash
# create
docker volume create autoclip_data
docker volume create autoclip_logs

# docker-compose.ymlconfig
volumes:
  - autoclip_data:/app/data
  - autoclip_logs:/app/logs
```

3. **config**
```yaml
# use
networks:
  autoclip-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 🛠️ dev environmentdeploy

### useconfig

```bash
# usedev environmentconfig
docker-compose -f docker-compose.dev.yml up -d

# view
docker-compose -f docker-compose.dev.yml logs -f

# 
docker-compose -f docker-compose.dev.yml exec autoclip-dev bash
```

### dev environment

- support
- 
- 
- 

## ⚙️ config notes

### env var

create `.env` file：

```bash
# databaseconfig
DATABASE_URL=sqlite:///./data/autoclip.db

# Redisconfig
REDIS_URL=redis://redis:6379/0

# LLM config（optional）：can http://localhost:3000 「settings → model」， ./data/settings.json，
# api  worker ；env var settings.json default。
# compose  api  worker。
# LLM_PROVIDER: dashscope | openai | gemini | siliconflow
LLM_PROVIDER=dashscope
API_MODEL_NAME=qwen-plus
API_DASHSCOPE_API_KEY=your_dashscope_api_key
# API_OPENAI_API_KEY=
# API_GEMINI_API_KEY=
# API_SILICONFLOW_API_KEY=
# OpenAI API（LLM_PROVIDER=openai ）： / DeepSeek / OpenRouter / local Ollama、vLLM 。
#   :    OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4   API_MODEL_NAME=glm-4-flash
#   DeepSeek: OPENAI_BASE_URL=https://api.deepseek.com/v1          API_MODEL_NAME=deepseek-chat
#    Ollama: OPENAI_BASE_URL=http://host.docker.internal:11434/v1  API_MODEL_NAME=qwen2.5:7b（ key）
# OPENAI_BASE_URL=
# Qwen（alibabacloud.com  Key）：
# DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1

# config
LOG_LEVEL=INFO
ENVIRONMENT=production
DEBUG=false

# file
UPLOAD_DIR=./data/uploads
PROJECT_DIR=./data/projects
```

### serviceconfig

#### service
- **port**: 8000 (backend), 3000 (frontend)
- **check**: `/api/v1/health/`
- ****: `unless-stopped`

#### Redisservice
- **port**: 6379
- ****: AOF
- **memorylimit**: config

#### Celeryservice
- **Worker**: 
- **Beat**: 
- ****: config

## 💾 data management

### 

```bash
# view
docker volume ls

# 
docker run --rm -v autoclip_data:/data -v $(pwd):/backup alpine tar czf /backup/autoclip-backup.tar.gz -C /data .

# 
docker run --rm -v autoclip_data:/data -v $(pwd):/backup alpine tar xzf /backup/autoclip-backup.tar.gz -C /data
```

### data directory

```
data/
├── autoclip.db          # SQLitedatabase
├── projects/            # project
├── uploads/             # upload file
├── temp/                # file
└── output/              # file
```

### 

```bash
# file
docker-compose exec autoclip find /app/data/temp -type f -mtime +7 -delete

# 
docker-compose exec autoclip find /app/logs -name "*.log" -mtime +30 -delete
```

## 🔧 troubleshooting

### FAQ

#### 1. servicestartfailed

```bash
# viewservicestatus
docker-compose ps

# view
docker-compose logs autoclip

# service
docker-compose restart autoclip
```

#### 2. port

```bash
# checkport
netstat -tulpn | grep :8000

# port
# docker-compose.ymlportsconfig
ports:
  - "8001:8000"  # local8001port8000port
```

#### 3. out of memory

```bash
# viewuse
docker stats

# limituse
# docker-compose.ymldeployconfig
```

#### 4. 

```bash
# check
docker volume inspect autoclip_data

# 
# use
```

### view

```bash
# viewservice
docker-compose logs

# viewservice
docker-compose logs autoclip
docker-compose logs celery-worker

# view
docker-compose logs -f

# view100
docker-compose logs --tail=100
```

### perf monitor

```bash
# viewuse
docker stats

# viewservicestatus
docker-compose ps

# 
docker-compose exec autoclip bash
```

## 🔄 update

### updateservice

```bash
# 
git pull

# build
docker-compose build

# service
docker-compose up -d
```

### 

```bash
#!/bin/bash
# backup.sh - 

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/autoclip"

# create
mkdir -p $BACKUP_DIR

# 
docker run --rm -v autoclip_data:/data -v $BACKUP_DIR:/backup alpine \
    tar czf /backup/autoclip-data-$DATE.tar.gz -C /data .

# config
cp .env $BACKUP_DIR/autoclip-config-$DATE.env

# （7）
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.env" -mtime +7 -delete

echo "completed: $DATE"
```

### monitor

```bash
#!/bin/bash
# monitor.sh - servicemonitor

# checkservicestatus
if ! docker-compose ps | grep -q "Up"; then
    echo "service，..."
    docker-compose restart
fi

# checkstatus
if ! curl -f http://localhost:8000/api/v1/health/ >/dev/null 2>&1; then
    echo "checkfailed，..."
    # can
fi
```

## 📚 config

### usedatabase

```yaml
# usePostgreSQL
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: autoclip
      POSTGRES_USER: autoclip
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  autoclip:
    environment:
      - DATABASE_URL=postgresql://autoclip:password@postgres:5432/autoclip
    depends_on:
      - postgres
```

### useRedis

```yaml
# useRedis
services:
  autoclip:
    environment:
      - REDIS_URL=redis://redis-cluster:6379/0
    external_links:
      - redis-cluster:redis
```

### 

```yaml
# useNginx
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - autoclip

  autoclip:
    # canstart
    scale: 3
```

## 🆘 get help

if you encounter issues，：

1. viewdocstroubleshooting
2. checkGitHub Issues
3. viewprojectdocs
4. tech support

---

**last updated**: 2024-01-15
