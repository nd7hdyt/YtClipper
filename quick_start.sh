#!/bin/bash

# AutoClip ENStartScript
# Version: 2.0
# EN: ENStartENEnvironment，ENCheck

set -euo pipefail

# =============================================================================
# ConfigEN
# =============================================================================

BACKEND_PORT=8000
FRONTEND_PORT=3000

# =============================================================================
# EN
# =============================================================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# =============================================================================
# ToolEN
# =============================================================================

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# =============================================================================
# EN
# =============================================================================

main() {
    echo -e "${GREEN}🚀 AutoClip ENStart${NC}"
    echo ""
    
    # CheckENEnvironment
    if [[ ! -d "venv" ]]; then
        log_warning "ENEnvironmentEN，PleaseEN: python3 -m venv venv"
        exit 1
    fi
    
    # ENEnvironment
    log_info "ENEnvironment..."
    source venv/bin/activate
    
    # ENPythonEN
    : "${PYTHONPATH:=}"
    export PYTHONPATH="${PWD}:${PYTHONPATH}"
    
    # ENEnvironmentEN
    if [[ -f ".env" ]]; then
        set -a
        source .env
        set +a
    fi
    
    # StartRedis（IfNeed）
    if ! redis-cli ping >/dev/null 2>&1; then
        log_info "StartRedis..."
        if command -v brew >/dev/null; then
            brew services start redis
            sleep 2
        fi
    fi
    
    # EN
    mkdir -p logs
    
    # StartEN
    log_info "StartENService..."
    nohup python -m uvicorn backend.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload > logs/backend.log 2>&1 &
    echo $! > backend.pid
    
    # StartCelery Worker
    log_info "StartCelery Worker..."
    nohup celery -A backend.core.celery_app worker --loglevel=info --concurrency=1 --prefetch-multiplier=1 -Q celery,processing,video,notification,upload > logs/celery.log 2>&1 &
    echo $! > celery.pid
    
    # StartEN
    log_info "StartENService..."
    cd frontend
    nohup npm run dev -- --host 0.0.0.0 --port "$FRONTEND_PORT" > ../logs/frontend.log 2>&1 &
    echo $! > ../frontend.pid
    cd ..
    
    # ENServiceStart
    log_info "ENServiceStart..."
    sleep 5
    
    # CheckServiceStatus
    if curl -fsS "http://localhost:$BACKEND_PORT/api/v1/health/" >/dev/null 2>&1; then
        log_success "ENServiceENStart"
    else
        log_warning "ENServiceStartEN"
    fi
    
    if curl -fsS "http://localhost:$FRONTEND_PORT/" >/dev/null 2>&1; then
        log_success "ENServiceENStart"
    else
        log_warning "ENServiceStartEN"
    fi
    
    echo ""
    log_success "ENStartCompleted！"
    echo ""
    echo "🌐 EN:"
    echo "  EN: http://localhost:$FRONTEND_PORT"
    echo "  EN: http://localhost:$BACKEND_PORT"
    echo "  APIEN: http://localhost:$BACKEND_PORT/docs"
    echo ""
    echo "📝 EN:"
    echo "  tail -f logs/backend.log"
    echo "  tail -f logs/frontend.log"
    echo "  tail -f logs/celery.log"
    echo ""
    echo "🛑 StopService: ./stop_autoclip.sh"
}

# EN
main "$@"
