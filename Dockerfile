# AutoClip Dockerfile
# EN，EN

# EN：EN
FROM node:18-slim AS frontend-builder

WORKDIR /app/frontend

# InstallENSystemDependencies
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# ENDependenciesEN
COPY frontend/package*.json ./

# InstallENDependencies（ENInstall，ENdevDependencies）
RUN npm ci

# EN
COPY frontend/ ./

# EN
RUN npm run build

# EN：EN
# yt-dlp ENStopEN Python 3.9（3.9 EN YouTube EN android client EN，EN 360p）
FROM python:3.11-slim AS backend-builder

# ENEnvironmentEN
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# InstallSystemDependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# ENPythonDependenciesEN
COPY requirements.txt ./

# InstallPythonDependencies
RUN pip install --no-cache-dir -r requirements.txt

# EN：EN
FROM python:3.11-slim

# ENEnvironmentEN
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# ENrootEN
RUN groupadd -r autoclip && useradd -r -g autoclip autoclip

# InstallENDependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# EN
WORKDIR /app

# EN
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# ENProjectEN
COPY backend/ ./backend/
COPY scripts/ ./scripts/
COPY *.sh ./
COPY env.example .env
COPY docker-entrypoint.sh ./

# EN
RUN mkdir -p data/projects data/uploads data/temp data/output logs

# EN
RUN chown -R autoclip:autoclip /app
RUN chmod +x *.sh
RUN chmod +x docker-entrypoint.sh
RUN chmod -R 755 data logs

# ENrootEN
USER autoclip

# EN
EXPOSE 8000 3000

# ENCheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/ || exit 1

# StartEN
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
