# Docker Deployment

ENDockerENAutoClipEN。

## 📋 EN

- [Quick Start](#Quick Start)
- [EN](#EN)
- [EN](#EN)
- [Configuration](#Configuration)
- [EN](#EN)
- [Troubleshooting](#Troubleshooting)

## 🚀 Quick Start

### Requirements

- Docker 20.10+
- Docker Compose 2.0+
- EN 4GB EN
- EN 10GB EN

### One-Click Start

```bash
# EN
git clone https://github.com/your-username/autoclip.git
cd autoclip

# EN
cp env.example .env
# EN .env EN，EN

# Linux EN：EN root EN，bind mount EN
mkdir -p data logs uploads && chmod -R 777 data logs uploads

# EN
docker-compose up -d

# EN
docker-compose ps

# EN
docker-compose logs -f
```

### EN

- **ENInterface**: http://localhost:3000
- **ENAPI**: http://localhost:8000
- **APIEN**: http://localhost:8000/docs
- **FlowerEN**: http://localhost:5555

## 🏭 EN

### EN

```bash
# EN
docker-compose -f docker-compose.yml up -d

# EN
docker-compose up -d

# EN
docker-compose ps

# EN
docker-compose logs -f autoclip
```

### EN

1. **EN**
```yaml
# ENdocker-compose.ymlEN
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

2. **EN**
```bash
# EN
docker volume create autoclip_data
docker volume create autoclip_logs

# ENdocker-compose.ymlEN
volumes:
  - autoclip_data:/app/data
  - autoclip_logs:/app/logs
```

3. **EN**
```yaml
# EN
networks:
  autoclip-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 🛠️ EN

### EN

```bash
# EN
docker-compose -f docker-compose.dev.yml up -d

# EN
docker-compose -f docker-compose.dev.yml logs -f

# EN
docker-compose -f docker-compose.dev.yml exec autoclip-dev bash
```

### EN

- ENSupport
- EN
- EN
- EN

## ⚙️ Configuration

### EN

EN `.env` EN：

```bash
# EN
DATABASE_URL=sqlite:///./data/autoclip.db

# RedisEN
REDIS_URL=redis://redis:6379/0

# LLM EN（EN）：EN http://localhost:3000 EN「EN → EN」EN，EN ./data/settings.json，
# api EN worker EN；EN settings.json EN。
# compose EN api EN worker。
# LLM_PROVIDER: dashscope | openai | gemini | siliconflow
LLM_PROVIDER=dashscope
API_MODEL_NAME=qwen-plus
API_DASHSCOPE_API_KEY=your_dashscope_api_key
# API_OPENAI_API_KEY=
# API_GEMINI_API_KEY=
# API_SILICONFLOW_API_KEY=
# OpenAI EN（LLM_PROVIDER=openai EN）：EN / DeepSeek / OpenRouter / EN Ollama、vLLM EN。
#   EN:    OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4   API_MODEL_NAME=glm-4-flash
#   DeepSeek: OPENAI_BASE_URL=https://api.deepseek.com/v1          API_MODEL_NAME=deepseek-chat
#   EN Ollama: OPENAI_BASE_URL=http://host.docker.internal:11434/v1  API_MODEL_NAME=qwen2.5:7b（EN key）
# OPENAI_BASE_URL=
# EN（alibabacloud.com EN Key）：
# DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1

# EN
LOG_LEVEL=INFO
ENVIRONMENT=production
DEBUG=false

# EN
UPLOAD_DIR=./data/uploads
PROJECT_DIR=./data/projects
```

### EN

#### EN
- **EN**: 8000 (EN), 3000 (EN)
- **Health Check**: `/api/v1/health/`
- **EN**: `unless-stopped`

#### RedisEN
- **EN**: 6379
- **EN**: AOFEN
- **EN**: EN

#### CeleryEN
- **Worker**: EN
- **Beat**: EN
- **EN**: EN

## 💾 EN

### EN

```bash
# EN
docker volume ls

# EN
docker run --rm -v autoclip_data:/data -v $(pwd):/backup alpine tar czf /backup/autoclip-backup.tar.gz -C /data .

# EN
docker run --rm -v autoclip_data:/data -v $(pwd):/backup alpine tar xzf /backup/autoclip-backup.tar.gz -C /data
```

### EN

```
data/
├── autoclip.db          # SQLiteEN
├── projects/            # EN
├── uploads/             # UploadEN
├── temp/                # EN
└── output/              # EN
```

### EN

```bash
# EN
docker-compose exec autoclip find /app/data/temp -type f -mtime +7 -delete

# EN
docker-compose exec autoclip find /app/logs -name "*.log" -mtime +30 -delete
```

## 🔧 Troubleshooting

### FAQ

#### 1. EN

```bash
# EN
docker-compose ps

# EN
docker-compose logs autoclip

# EN
docker-compose restart autoclip
```

#### 2. EN

```bash
# EN
netstat -tulpn | grep :8000

# EN
# ENdocker-compose.ymlENportsEN
ports:
  - "8001:8000"  # EN8001EN8000EN
```

#### 3. EN

```bash
# EN
docker stats

# EN
# ENdocker-compose.ymlENdeployEN
```

#### 4. EN

```bash
# EN
docker volume inspect autoclip_data

# EN
# EN
```

### EN

```bash
# EN
docker-compose logs

# EN
docker-compose logs autoclip
docker-compose logs celery-worker

# EN
docker-compose logs -f

# EN100EN
docker-compose logs --tail=100
```

### EN

```bash
# EN
docker stats

# EN
docker-compose ps

# EN
docker-compose exec autoclip bash
```

## 🔄 EN

### EN

```bash
# EN
git pull

# EN
docker-compose build

# EN
docker-compose up -d
```

### EN

```bash
#!/bin/bash
# backup.sh - EN

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/autoclip"

# EN
mkdir -p $BACKUP_DIR

# EN
docker run --rm -v autoclip_data:/data -v $BACKUP_DIR:/backup alpine \
    tar czf /backup/autoclip-data-$DATE.tar.gz -C /data .

# EN
cp .env $BACKUP_DIR/autoclip-config-$DATE.env

# EN（EN7EN）
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.env" -mtime +7 -delete

echo "EN: $DATE"
```

### EN

```bash
#!/bin/bash
# monitor.sh - EN

# EN
if ! docker-compose ps | grep -q "Up"; then
    echo "EN，EN..."
    docker-compose restart
fi

# EN
if ! curl -f http://localhost:8000/api/v1/health/ >/dev/null 2>&1; then
    echo "Health CheckEN，EN..."
    # EN
fi
```

## 📚 EN

### EN

```yaml
# ENPostgreSQL
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

### ENRedis

```yaml
# ENRedisEN
services:
  autoclip:
    environment:
      - REDIS_URL=redis://redis-cluster:6379/0
    external_links:
      - redis-cluster:redis
```

### EN

```yaml
# ENNginxEN
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
    # EN
    scale: 3
```

## 🆘 EN

EN，EN：

1. ENTroubleshootingEN
2. ENGitHub Issues
3. EN
4. ContactENSupport

---

**EN**: 2024-01-15
