#!/bin/bash

# AutoClip ENStartScript
# Version: 2.0
# EN: StartENAutoClipSystem（ENAPI + Celery Worker + EN）

set -euo pipefail

# =============================================================================
# ConfigEN
# =============================================================================

# ServiceENConfig
BACKEND_PORT=8000
FRONTEND_PORT=3000
REDIS_PORT=6379

# ServiceENConfig
BACKEND_STARTUP_TIMEOUT=60
FRONTEND_STARTUP_TIMEOUT=90
HEALTH_CHECK_TIMEOUT=10

# ENConfig
LOG_DIR="logs"
BACKEND_LOG="$LOG_DIR/backend.log"
FRONTEND_LOG="$LOG_DIR/frontend.log"
CELERY_LOG="$LOG_DIR/celery.log"

# PIDEN
BACKEND_PID_FILE="backend.pid"
FRONTEND_PID_FILE="frontend.pid"
CELERY_PID_FILE="celery.pid"

# =============================================================================
# EN
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# EN
ICON_SUCCESS="✅"
ICON_ERROR="❌"
ICON_WARNING="⚠️"
ICON_INFO="ℹ️"
ICON_ROCKET="🚀"
ICON_GEAR="⚙️"
ICON_DATABASE="🗄️"
ICON_WORKER="👷"
ICON_WEB="🌐"
ICON_HEALTH="💚"

# =============================================================================
# ToolEN
# =============================================================================

log_info() {
    echo -e "${BLUE}${ICON_INFO} $1${NC}"
}

log_success() {
    echo -e "${GREEN}${ICON_SUCCESS} $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}${ICON_WARNING} $1${NC}"
}

log_error() {
    echo -e "${RED}${ICON_ERROR} $1${NC}"
}

log_header() {
    echo -e "\n${PURPLE}${ICON_ROCKET} $1${NC}"
    echo -e "${PURPLE}$(printf '=%.0s' {1..50})${NC}"
}

log_step() {
    echo -e "\n${CYAN}${ICON_GEAR} $1${NC}"
}

# CheckEN
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# CheckEN
port_in_use() {
    lsof -i ":$1" >/dev/null 2>&1
}

# ENServiceStart
wait_for_service() {
    local url="$1"
    local timeout="$2"
    local service_name="$3"
    
    log_info "EN $service_name Start..."
    
    for i in $(seq 1 "$timeout"); do
        if curl -fsS "$url" >/dev/null 2>&1; then
            log_success "$service_name ENStart"
            return 0
        fi
        sleep 1
    done
    
    log_error "$service_name StartEN"
    return 1
}

# CheckEN
process_running() {
    local pid_file="$1"
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            return 0
        else
            rm -f "$pid_file"
        fi
    fi
    return 1
}

# StopEN
stop_process() {
    local pid_file="$1"
    local service_name="$2"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            log_info "Stop $service_name (PID: $pid)..."
            kill "$pid" 2>/dev/null || true
            sleep 2
            if kill -0 "$pid" 2>/dev/null; then
                log_warning "ENStop $service_name..."
                kill -9 "$pid" 2>/dev/null || true
            fi
        fi
        rm -f "$pid_file"
    fi
}

# =============================================================================
# EnvironmentCheckEN
# =============================================================================

check_environment() {
    log_header "EnvironmentCheck"
    
    # CheckENSystem
    if [[ "$OSTYPE" == "darwin"* ]]; then
        log_success "EN macOS System"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_success "EN Linux System"
    else
        log_warning "ENSystem: $OSTYPE"
    fi
    
    # CheckEN（ENDockerEnvironmentENnodeCheck）
    if [[ "${ENVIRONMENT:-}" != "production" ]] || [[ ! -f "/.dockerenv" ]]; then
        local required_commands=("python3" "node" "npm" "redis-cli")
        for cmd in "${required_commands[@]}"; do
            if command_exists "$cmd"; then
                log_success "$cmd ENInstall"
            else
                log_error "$cmd ENInstall，PleaseENInstall"
                exit 1
            fi
        done
    else
        log_info "DockerEnvironmentEN，ENnodeEnvironmentCheck"
        local required_commands=("python3" "redis-cli")
        for cmd in "${required_commands[@]}"; do
            if command_exists "$cmd"; then
                log_success "$cmd ENInstall"
            else
                log_error "$cmd ENInstall，PleaseENInstall"
                exit 1
            fi
        done
    fi
    
    # CheckPythonVersion
    local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    log_info "Python Version: $python_version"
    
    # CheckNode.jsVersion
    local node_version=$(node --version)
    log_info "Node.js Version: $node_version"
    
    # CheckENEnvironment
    if [[ ! -d "venv" ]]; then
        log_error "ENEnvironmentEN，PleaseEN: python3 -m venv venv"
        exit 1
    fi
    log_success "ENEnvironmentEN"
    
    # CheckProjectEN
    local required_dirs=("backend" "frontend" "data")
    for dir in "${required_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            log_success "EN $dir EN"
        else
            log_error "EN $dir EN"
            exit 1
        fi
    done
}

# =============================================================================
# ServiceStartEN
# =============================================================================

start_redis() {
    log_step "Start Redis Service"
    
    if redis-cli ping >/dev/null 2>&1; then
        log_success "Redis ServiceEN"
        return 0
    fi
    
    log_info "Start Redis Service..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command_exists brew; then
            brew services start redis
            sleep 3
        else
            log_error "PleaseManualStart Redis Service"
            exit 1
        fi
    else
        systemctl start redis-server 2>/dev/null || service redis-server start 2>/dev/null || {
            log_error "ENStart Redis Service，PleaseManualStart"
            exit 1
        }
    fi
    
    if redis-cli ping >/dev/null 2>&1; then
        log_success "Redis ServiceStartSuccess"
    else
        log_error "Redis ServiceStartFailed"
        exit 1
    fi
}

setup_environment() {
    log_step "ENEnvironment"
    
    # EN
    mkdir -p "$LOG_DIR"
    
    # ENEnvironment
    log_info "ENEnvironment..."
    source venv/bin/activate
    
    # ENPythonEN
    : "${PYTHONPATH:=}"
    export PYTHONPATH="${PWD}:${PYTHONPATH}"
    log_info "EN Python EN: $PYTHONPATH"
    
    # ENEnvironmentEN
    if [[ -f ".env" ]]; then
        log_info "ENEnvironmentEN..."
        set -a
        source .env
        set +a
        log_success "EnvironmentENSuccess"
    else
        log_warning ".env EN，ENConfig"
        # ENEnvironmentEN
        if [[ ! -f ".env" ]]; then
            log_info "EN .env EN..."
            cp env.example .env 2>/dev/null || {
                cat > .env << EOF
# AutoClip EnvironmentConfig
DATABASE_URL=sqlite:///./data/autoclip.db
REDIS_URL=redis://localhost:6379/0
API_DASHSCOPE_API_KEY=
API_MODEL_NAME=qwen-plus
LOG_LEVEL=INFO
ENVIRONMENT=development
DEBUG=true
EOF
                log_success "EN .env EN"
            }
        fi
    fi
    
    # CheckPythonDependencies
    log_info "Check Python Dependencies..."
    if ! python -c "import fastapi, celery, sqlalchemy" 2>/dev/null; then
        log_warning "ENDependencies，CurrentlyInstall..."
        pip install -r requirements.txt
    fi
    log_success "Python DependenciesCheckCompleted"
}

init_database() {
    log_step "EN"
    
    # EN
    mkdir -p data
    
    # EN
    log_info "EN..."
    if python -c "
import sys
sys.path.insert(0, '.')
from backend.core.database import engine, Base
from backend.models import project, task, clip, collection, bilibili
try:
    Base.metadata.create_all(bind=engine)
    print('ENSuccess')
except Exception as e:
    print(f'ENFailed: {e}')
    sys.exit(1)
" 2>/dev/null; then
        log_success "ENSuccess"
    else
        log_error "ENFailed"
        exit 1
    fi
}

start_celery() {
    log_step "Start Celery Worker"
    
    # StopENCeleryEN
    pkill -f "celery.*worker" 2>/dev/null || true
    sleep 2
    
    # ENWhisperEN
    log_info "CheckENWhisperEN..."
    python scripts/monitor_whisper.py --kill-duplicates 2>/dev/null || true
    
    log_info "Start Celery Worker..."
    nohup celery -A backend.core.celery_app worker \
        --loglevel=info \
        --concurrency=1 \
        --prefetch-multiplier=1 \
        -Q celery,processing,video,notification,upload \
        --hostname=worker@%h \
        > "$CELERY_LOG" 2>&1 &
    
    local celery_pid=$!
    echo "$celery_pid" > "$CELERY_PID_FILE"
    
    # ENWorkerStart
    sleep 5
    
    if pgrep -f "celery.*worker" >/dev/null; then
        log_success "Celery Worker ENStart (PID: $celery_pid)"
    else
        log_error "Celery Worker StartFailed"
        log_info "EN: tail -f $CELERY_LOG"
        exit 1
    fi
}

start_backend() {
    log_step "StartEN API Service"
    
    # CheckEN
    if port_in_use "$BACKEND_PORT"; then
        log_warning "EN $BACKEND_PORT EN，ENStopENService..."
        stop_process "$BACKEND_PID_FILE" "ENService"
    fi
    
    log_info "StartENService (EN: $BACKEND_PORT)..."
    nohup python -m uvicorn backend.main:app \
        --host 0.0.0.0 \
        --port "$BACKEND_PORT" \
        --reload \
        --reload-dir backend \
        --reload-include '*.py' \
        --reload-exclude 'data/*' \
        --reload-exclude 'logs/*' \
        --reload-exclude 'uploads/*' \
        --reload-exclude '*.log' \
        > "$BACKEND_LOG" 2>&1 &
    
    local backend_pid=$!
    echo "$backend_pid" > "$BACKEND_PID_FILE"
    
    # ENStart
    if wait_for_service "http://localhost:$BACKEND_PORT/api/v1/health/" "$BACKEND_STARTUP_TIMEOUT" "ENService"; then
        log_success "ENServiceENStart (PID: $backend_pid)"
    else
        log_error "ENServiceStartFailed"
        log_info "EN: tail -f $BACKEND_LOG"
        exit 1
    fi
}

start_frontend() {
    log_step "StartENService"
    
    # CheckEN
    if port_in_use "$FRONTEND_PORT"; then
        log_warning "EN $FRONTEND_PORT EN，ENStopENService..."
        stop_process "$FRONTEND_PID_FILE" "ENService"
    fi
    
    # EN
    cd frontend || {
        log_error "EN"
        exit 1
    }
    
    # CheckENDependencies
    if [[ ! -d "node_modules" ]]; then
        log_info "InstallENDependencies..."
        npm install
    fi
    
    log_info "StartENService (EN: $FRONTEND_PORT)..."
    nohup npm run dev -- --host 0.0.0.0 --port "$FRONTEND_PORT" \
        > "../$FRONTEND_LOG" 2>&1 &
    
    local frontend_pid=$!
    echo "$frontend_pid" > "../$FRONTEND_PID_FILE"
    
    # ENProjectEN
    cd ..
    
    # ENStart
    if wait_for_service "http://localhost:$FRONTEND_PORT/" "$FRONTEND_STARTUP_TIMEOUT" "ENService"; then
        log_success "ENServiceENStart (PID: $frontend_pid)"
    else
        log_error "ENServiceStartFailed"
        log_info "EN: tail -f $FRONTEND_LOG"
        exit 1
    fi
}

# =============================================================================
# ENCheckEN
# =============================================================================

health_check() {
    log_header "SystemENCheck"
    
    local all_healthy=true
    
    # CheckEN
    log_info "CheckENService..."
    if curl -fsS "http://localhost:$BACKEND_PORT/api/v1/health/" >/dev/null 2>&1; then
        log_success "ENServiceEN"
    else
        log_error "ENServiceEN"
        all_healthy=false
    fi
    
    # CheckEN
    log_info "CheckENService..."
    if curl -fsS "http://localhost:$FRONTEND_PORT/" >/dev/null 2>&1; then
        log_success "ENServiceEN"
    else
        log_error "ENServiceEN"
        all_healthy=false
    fi
    
    # CheckRedis
    log_info "Check Redis Service..."
    if redis-cli ping >/dev/null 2>&1; then
        log_success "Redis ServiceEN"
    else
        log_error "Redis ServiceEN"
        all_healthy=false
    fi
    
    # CheckCelery Worker
    log_info "Check Celery Worker..."
    if pgrep -f "celery.*worker" >/dev/null; then
        log_success "Celery Worker EN"
    else
        log_error "Celery Worker EN"
        all_healthy=false
    fi
    
    if [[ "$all_healthy" == true ]]; then
        log_success "AllServiceENCheckEN"
        return 0
    else
        log_error "ENServiceENCheckFailed"
        return 1
    fi
}

# =============================================================================
# EN
# =============================================================================

cleanup() {
    log_header "ENService"
    
    stop_process "$BACKEND_PID_FILE" "ENService"
    stop_process "$FRONTEND_PID_FILE" "ENService"
    stop_process "$CELERY_PID_FILE" "Celery Worker"
    
    # StopAllEN
    pkill -f "celery.*worker" 2>/dev/null || true
    pkill -f "uvicorn.*backend.main:app" 2>/dev/null || true
    pkill -f "npm.*dev" 2>/dev/null || true
    
    log_success "ENCompleted"
}

# =============================================================================
# ENSystemEN
# =============================================================================

show_system_info() {
    log_header "SystemStartCompleted"
    
    echo -e "${WHITE}🎉 AutoClip SystemENSuccessStart！${NC}"
    echo ""
    echo -e "${CYAN}📊 ServiceStatus:${NC}"
    echo -e "  ${ICON_WEB} EN API:     http://localhost:$BACKEND_PORT"
    echo -e "  ${ICON_WEB} EN:     http://localhost:$FRONTEND_PORT"
    echo -e "  ${ICON_WEB} API EN:     http://localhost:$BACKEND_PORT/docs"
    echo -e "  ${ICON_HEALTH} ENCheck:   http://localhost:$BACKEND_PORT/api/v1/health/"
    echo ""
    echo -e "${CYAN}📝 EN:${NC}"
    echo -e "  EN: tail -f $BACKEND_LOG"
    echo -e "  EN: tail -f $FRONTEND_LOG"
    echo -e "  CeleryEN: tail -f $CELERY_LOG"
    echo ""
    echo -e "${CYAN}🛑 StopSystem:${NC}"
    echo -e "  ./stop_autoclip.sh EN Ctrl+C"
    echo ""
    echo -e "${YELLOW}💡 EN:${NC}"
    echo -e "  1. EN http://localhost:$FRONTEND_PORT EN"
    echo -e "  2. UploadENBEN"
    echo -e "  3. SystemENAutoStartAIProcessingEN"
    echo -e "  4. ENProcessingEN"
    echo ""
}

# =============================================================================
# ENProcessing
# =============================================================================

trap cleanup EXIT INT TERM

# =============================================================================
# EN
# =============================================================================

main() {
    log_header "AutoClip SystemStartEN v2.0"
    
    # EnvironmentCheck
    check_environment
    
    # StartService
    start_redis
    setup_environment
    init_database
    start_celery
    start_backend
    start_frontend
    
    # ENCheck
    if health_check; then
        show_system_info
        
        # ENScriptEN（ENCheck）
        log_info "SystemEN... EN Ctrl+C Stop"
        log_info "ENCheckSystemStatus，PleaseEN: ./status_autoclip.sh"
        while true; do
            sleep 3600  # ENCheckEN，EN
        done
    else
        log_error "SystemStartFailed，PleaseCheckEN"
        exit 1
    fi
}

# EN
main "$@"
