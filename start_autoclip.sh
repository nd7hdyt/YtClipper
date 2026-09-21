#!/bin/bash

# AutoClip One-Click Starttranslated
# version: 2.0
# feature: starttranslated'sAutoClipSystem（backendAPI + Celery Worker + frontendInterface）

set -euo pipefail

# =============================================================================
# configtranslated
# =============================================================================

# servicetranslatedconfig
BACKtranslatedD_PORT=8000
FRONTtranslatedD_PORT=3000
REDIS_PORT=6379

# servicetranslatedconfig
BACKtranslatedD_STARTUP_TIMEOUT=60
FRONTtranslatedD_STARTUP_TIMEOUT=90
HEALTH_CHECK_TIMEOUT=10

# logsconfig
LOG_DIR="logs"
BACKtranslatedD_LOG="$LOG_DIR/backend.log"
FRONTtranslatedD_LOG="$LOG_DIR/frontend.log"
CELERY_LOG="$LOG_DIR/celery.log"

# PIDfile
BACKtranslatedD_PID_FILE="backend.pid"
FRONTtranslatedD_PID_FILE="frontend.pid"
CELERY_PID_FILE="celery.pid"

# =============================================================================
# translatedAndtranslated
# =============================================================================

RED='\033[0;31m'
GREtranslated='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# translated
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
# tooltranslated
# =============================================================================

log_info() {
    echo -e "${BLUE}${ICON_INFO} $1${NC}"
}

log_success() {
    echo -e "${GREtranslated}${ICON_SUCCESS} $1${NC}"
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

# checktranslatedIstranslatedin
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# checktranslatedIstranslateduse
port_in_use() {
    lsof -i ":$1" >/dev/null 2>&1
}

# etc.translatedservicestart
wait_for_service() {
    local url="$1"
    local timeout="$2"
    local service_name="$3"
    
    log_info "etc.translated $service_name start..."
    
    for i in $(seq 1 "$timeout"); do
        if curl -fsS "$url" >/dev/null 2>&1; then
            log_success "$service_name translatedstart"
            return 0
        fi
        sleep 1
    done
    
    log_error "$service_name starttranslated"
    return 1
}

# checkprocessIstranslated
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

# translatedprocess
stop_process() {
    local pid_file="$1"
    local service_name="$2"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            log_info "translated $service_name (PID: $pid)..."
            kill "$pid" 2>/dev/null || true
            sleep 2
            if kill -0 "$pid" 2>/dev/null; then
                log_warning "translated $service_name..."
                kill -9 "$pid" 2>/dev/null || true
            fi
        fi
        rm -f "$pid_file"
    fi
}

# =============================================================================
# translatedchecktranslated
# =============================================================================

check_environment() {
    log_header "translatedcheck"
    
    # checktranslatedSystem
    if [[ "$OSTYPE" == "darwin"* ]]; then
        log_success "translated macOS System"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_success "translated Linux System"
    else
        log_warning "translated'stranslatedSystem: $OSTYPE"
    fi
    
    # checktranslated'stranslated（inDockertranslatedskipnodecheck）
    if [[ "${translatedVIRONMtranslatedT:-}" != "production" ]] || [[ ! -f "/.dockerenv" ]]; then
        local required_commands=("python3" "node" "npm" "redis-cli")
        for cmd in "${required_commands[@]}"; do
            if command_exists "$cmd"; then
                log_success "$cmd translatedinstall"
            else
                log_error "$cmd translatedinstall，translatedinstall"
                exit 1
            fi
        done
    else
        log_info "Dockertranslated，skipnodetranslatedcheck"
        local required_commands=("python3" "redis-cli")
        for cmd in "${required_commands[@]}"; do
            if command_exists "$cmd"; then
                log_success "$cmd translatedinstall"
            else
                log_error "$cmd translatedinstall，translatedinstall"
                exit 1
            fi
        done
    fi
    
    # checkPythonversion
    local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    log_info "Python version: $python_version"
    
    # checkNode.jsversion
    local node_version=$(node --version)
    log_info "Node.js version: $node_version"
    
    # checktranslated
    if [[ ! -d "venv" ]]; then
        log_error "translatednot found，translatedcreate: python3 -m venv venv"
        exit 1
    fi
    log_success "translatedin"
    
    # checkProject Structure
    local required_dirs=("backend" "frontend" "data")
    for dir in "${required_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            log_success "directory $dir translatedin"
        else
            log_error "directory $dir not found"
            exit 1
        fi
    done
}

# =============================================================================
# servicestarttranslated
# =============================================================================

start_redis() {
    log_step "start Redis service"
    
    if redis-cli ping >/dev/null 2>&1; then
        log_success "Redis servicetranslated"
        return 0
    fi
    
    log_info "start Redis service..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command_exists brew; then
            brew services start redis
            sleep 3
        else
            log_error "translatedstart Redis service"
            exit 1
        fi
    else
        systemctl start redis-server 2>/dev/null || service redis-server start 2>/dev/null || {
            log_error "translatedstart Redis service，translatedstart"
            exit 1
        }
    fi
    
    if redis-cli ping >/dev/null 2>&1; then
        log_success "Redis servicestartsucceeded"
    else
        log_error "Redis servicestartfailed"
        exit 1
    fi
}

setup_environment() {
    log_step "settingstranslated"
    
    # createlogsdirectory
    mkdir -p "$LOG_DIR"
    
    # translated
    log_info "translated..."
    source venv/bin/activate
    
    # settingsPythonpath
    : "${PYTHONPATH:=}"
    export PYTHONPATH="${PWD}:${PYTHONPATH}"
    log_info "settings Python path: $PYTHONPATH"
    
    # translated
    if [[ -f ".env" ]]; then
        log_info "translated..."
        set -a
        source .env
        set +a
        log_success "translatedsucceeded"
    else
        log_warning ".env file not found，usedefaultconfig"
        # createdefaulttranslatedfile
        if [[ ! -f ".env" ]]; then
            log_info "createdefault .env file..."
            cp env.example .env 2>/dev/null || {
                cat > .env << EOF
# AutoClip translatedconfig
DATABASE_URL=sqlite:///./data/autoclip.db
REDIS_URL=redis://localhost:6379/0
API_DASHSCOPE_API_KEY=
API_MODEL_NAME=qwen-plus
LOG_LEVEL=INFO
translatedVIRONMtranslatedT=development
DEBUG=true
EOF
                log_success "translatedcreatedefault .env file"
            }
        fi
    fi
    
    # checkPythondependencies
    log_info "check Python dependencies..."
    if ! python -c "import fastapi, celery, sqlalchemy" 2>/dev/null; then
        log_warning "translateddependencies，translatedininstall..."
        pip install -r requirements.txt
    fi
    log_success "Python dependencieschecktranslated"
}

init_database() {
    log_step "translateddatabase"
    
    # ensuretranslateddirectorytranslatedin
    mkdir -p data
    
    # translateddatabase
    log_info "createdatabasetranslated..."
    if python -c "
import sys
sys.path.insert(0, '.')
from backend.core.database import engine, Base
from backend.models import project, task, clip, collection, bilibili
try:
    Base.metadata.create_all(bind=engine)
    print('databasetranslatedcreatesucceeded')
except Exception as e:
    print(f'databasetranslatedfailed: {e}')
    sys.exit(1)
" 2>/dev/null; then
        log_success "databasetranslatedsucceeded"
    else
        log_error "databasetranslatedfailed"
        exit 1
    fi
}

start_celery() {
    log_step "start Celery Worker"
    
    # translated'sCeleryprocess
    pkill -f "celery.*worker" 2>/dev/null || true
    sleep 2
    
    # cleancantranslatedin'stranslatedWhisperprocess
    log_info "checktranslatedcleantranslated'sWhisperprocess..."
    python scripts/monitor_whisper.py --kill-duplicates 2>/dev/null || true
    
    log_info "start Celery Worker..."
    nohup celery -A backend.core.celery_app worker \
        --loglevel=info \
        --concurrency=1 \
        --prefetch-multiplier=1 \
        -Q celery,processing,video,notification,upload \
        --hostname=worker@%h \
        > "$CELERY_LOG" 2>&1 &
    
    local celery_pid=$!
    echo "$celery_pid" > "$CELERY_PID_FILE"
    
    # etc.translatedWorkerstart
    sleep 5
    
    if pgrep -f "celery.*worker" >/dev/null; then
        log_success "Celery Worker translatedstart (PID: $celery_pid)"
    else
        log_error "Celery Worker startfailed"
        log_info "translatedlogs: tail -f $CELERY_LOG"
        exit 1
    fi
}

start_backend() {
    log_step "startbackend API service"
    
    # checktranslatedIstranslateduse
    if port_in_use "$BACKtranslatedD_PORT"; then
        log_warning "translated $BACKtranslatedD_PORT translateduse，translatedservice..."
        stop_process "$BACKtranslatedD_PID_FILE" "backendservice"
    fi
    
    log_info "startbackendservice (translated: $BACKtranslatedD_PORT)..."
    nohup python -m uvicorn backend.main:app \
        --host 0.0.0.0 \
        --port "$BACKtranslatedD_PORT" \
        --reload \
        --reload-dir backend \
        --reload-include '*.py' \
        --reload-exclude 'data/*' \
        --reload-exclude 'logs/*' \
        --reload-exclude 'uploads/*' \
        --reload-exclude '*.log' \
        > "$BACKtranslatedD_LOG" 2>&1 &
    
    local backend_pid=$!
    echo "$backend_pid" > "$BACKtranslatedD_PID_FILE"
    
    # etc.translatedbackendstart
    if wait_for_service "http://localhost:$BACKtranslatedD_PORT/api/v1/health/" "$BACKtranslatedD_STARTUP_TIMEOUT" "backendservice"; then
        log_success "backendservicetranslatedstart (PID: $backend_pid)"
    else
        log_error "backendservicestartfailed"
        log_info "translatedlogs: tail -f $BACKtranslatedD_LOG"
        exit 1
    fi
}

start_frontend() {
    log_step "startfrontendservice"
    
    # checktranslatedIstranslateduse
    if port_in_use "$FRONTtranslatedD_PORT"; then
        log_warning "translated $FRONTtranslatedD_PORT translateduse，translatedservice..."
        stop_process "$FRONTtranslatedD_PID_FILE" "frontendservice"
    fi
    
    # translatedfrontenddirectory
    cd frontend || {
        log_error "translatedfrontenddirectory"
        exit 1
    }
    
    # checkfrontenddependencies
    if [[ ! -d "node_modules" ]]; then
        log_info "installfrontenddependencies..."
        npm install
    fi
    
    log_info "startfrontendservice (translated: $FRONTtranslatedD_PORT)..."
    nohup npm run dev -- --host 0.0.0.0 --port "$FRONTtranslatedD_PORT" \
        > "../$FRONTtranslatedD_LOG" 2>&1 &
    
    local frontend_pid=$!
    echo "$frontend_pid" > "../$FRONTtranslatedD_PID_FILE"
    
    # returnprojecttranslateddirectory
    cd ..
    
    # etc.translatedfrontendstart
    if wait_for_service "http://localhost:$FRONTtranslatedD_PORT/" "$FRONTtranslatedD_STARTUP_TIMEOUT" "frontendservice"; then
        log_success "frontendservicetranslatedstart (PID: $frontend_pid)"
    else
        log_error "frontendservicestartfailed"
        log_info "translatedlogs: tail -f $FRONTtranslatedD_LOG"
        exit 1
    fi
}

# =============================================================================
# Health Checktranslated
# =============================================================================

health_check() {
    log_header "SystemHealth Check"
    
    local all_healthy=true
    
    # checkbackend
    log_info "checkbackendservice..."
    if curl -fsS "http://localhost:$BACKtranslatedD_PORT/api/v1/health/" >/dev/null 2>&1; then
        log_success "backendservicetranslated"
    else
        log_error "backendservicetranslated"
        all_healthy=false
    fi
    
    # checkfrontend
    log_info "checkfrontendservice..."
    if curl -fsS "http://localhost:$FRONTtranslatedD_PORT/" >/dev/null 2>&1; then
        log_success "frontendservicetranslated"
    else
        log_error "frontendservicetranslated"
        all_healthy=false
    fi
    
    # checkRedis
    log_info "check Redis service..."
    if redis-cli ping >/dev/null 2>&1; then
        log_success "Redis servicetranslated"
    else
        log_error "Redis servicetranslated"
        all_healthy=false
    fi
    
    # checkCelery Worker
    log_info "check Celery Worker..."
    if pgrep -f "celery.*worker" >/dev/null; then
        log_success "Celery Worker translated"
    else
        log_error "Celery Worker translated"
        all_healthy=false
    fi
    
    if [[ "$all_healthy" == true ]]; then
        log_success "translatedserviceHealth Checktranslated"
        return 0
    else
        log_error "translatedserviceHealth Checkfailed"
        return 1
    fi
}

# =============================================================================
# cleantranslated
# =============================================================================

cleanup() {
    log_header "cleanservice"
    
    stop_process "$BACKtranslatedD_PID_FILE" "backendservice"
    stop_process "$FRONTtranslatedD_PID_FILE" "frontendservice"
    stop_process "$CELERY_PID_FILE" "Celery Worker"
    
    # translatedprocess
    pkill -f "celery.*worker" 2>/dev/null || true
    pkill -f "uvicorn.*backend.main:app" 2>/dev/null || true
    pkill -f "npm.*dev" 2>/dev/null || true
    
    log_success "cleantranslated"
}

# =============================================================================
# translatedSysteminfo
# =============================================================================

show_system_info() {
    log_header "Systemstarttranslated"
    
    echo -e "${WHITE}🎉 AutoClip Systemtranslatedsucceededstart！${NC}"
    echo ""
    echo -e "${CYAN}📊 servicestatus:${NC}"
    echo -e "  ${ICON_WEB} backend API:     http://localhost:$BACKtranslatedD_PORT"
    echo -e "  ${ICON_WEB} frontendInterface:     http://localhost:$FRONTtranslatedD_PORT"
    echo -e "  ${ICON_WEB} API docs:     http://localhost:$BACKtranslatedD_PORT/docs"
    echo -e "  ${ICON_HEALTH} Health Check:   http://localhost:$BACKtranslatedD_PORT/api/v1/health/"
    echo ""
    echo -e "${CYAN}📝 logsfile:${NC}"
    echo -e "  backendlogs: tail -f $BACKtranslatedD_LOG"
    echo -e "  frontendlogs: tail -f $FRONTtranslatedD_LOG"
    echo -e "  Celerylogs: tail -f $CELERY_LOG"
    echo ""
    echo -e "${CYAN}🛑 translatedSystem:${NC}"
    echo -e "  ./stop_autoclip.sh orby Ctrl+C"
    echo ""
    echo -e "${YELLOW}💡 usetranslated:${NC}"
    echo -e "  1. translated http://localhost:$FRONTtranslatedD_PORT usefrontendInterface"
    echo -e "  2. UploadvideofileortranslatedBsitetranslated"
    echo -e "  3. SystemtranslatedstartAIprocesstranslated"
    echo -e "  4. translatedprocessprogressAndtranslated"
    echo ""
}

# =============================================================================
# translatedprocess
# =============================================================================

trap cleanup EXIT INT TERM

# =============================================================================
# translated
# =============================================================================

main() {
    log_header "AutoClip Systemstarttranslated v2.0"
    
    # translatedcheck
    check_environment
    
    # startservice
    start_redis
    setup_environment
    init_database
    start_celery
    start_backend
    start_frontend
    
    # Health Check
    if health_check; then
        show_system_info
        
        # translated（translatedcheck）
        log_info "Systemtranslated... by Ctrl+C translated"
        log_info "iftranslatedcheckSystemstatus，translated: ./status_autoclip.sh"
        while true; do
            sleep 3600  # pertranslatedcheckonetranslated，translated
        done
    else
        log_error "Systemstartfailed，translatedchecklogs"
        exit 1
    fi
}

# translated
main "$@"
