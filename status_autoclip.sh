#!/bin/bash

# AutoClip SystemStatusCheckScript
# Version: 2.0
# EN: CheckAutoClipSystemENServiceENStatus

set -euo pipefail

# =============================================================================
# ConfigEN
# =============================================================================

# ServiceENConfig
BACKEND_PORT=8000
FRONTEND_PORT=3000
REDIS_PORT=6379

# PIDEN
BACKEND_PID_FILE="backend.pid"
FRONTEND_PID_FILE="frontend.pid"
CELERY_PID_FILE="celery.pid"

# EN
LOG_DIR="logs"

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
ICON_HEALTH="💚"
ICON_SICK="🤒"
ICON_ROCKET="🚀"
ICON_DATABASE="🗄️"
ICON_WORKER="👷"
ICON_WEB="🌐"
ICON_REDIS="🔴"

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

# CheckServiceENStatus
check_service_health() {
    local url="$1"
    local service_name="$2"
    
    if curl -fsS "$url" >/dev/null 2>&1; then
        echo -e "${GREEN}${ICON_HEALTH} $service_name EN${NC}"
        return 0
    else
        echo -e "${RED}${ICON_SICK} $service_name EN${NC}"
        return 1
    fi
}

# CheckENStatus
check_process_status() {
    local pid_file="$1"
    local service_name="$2"
    local process_pattern="$3"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${GREEN}${ICON_SUCCESS} $service_name EN (PID: $pid)${NC}"
            return 0
        else
            echo -e "${RED}${ICON_ERROR} $service_name PIDEN${NC}"
            return 1
        fi
    else
        # CheckEN
        if pgrep -f "$process_pattern" >/dev/null; then
            local pids=$(pgrep -f "$process_pattern" | tr '\n' ' ')
            echo -e "${YELLOW}${ICON_WARNING} $service_name ENPIDEN (PIDs: $pids)${NC}"
            return 0
        else
            echo -e "${RED}${ICON_ERROR} $service_name EN${NC}"
            return 1
        fi
    fi
}

# ENServiceEN
get_service_info() {
    local service_name="$1"
    local pid_file="$2"
    local process_pattern="$3"
    
    echo -e "\n${CYAN}📊 $service_name EN:${NC}"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo "  PID: $pid"
            echo "  EN:"
            ps -p "$pid" -o pid,ppid,etime,pcpu,pmem,cmd --no-headers 2>/dev/null | while read line; do
                echo "    $line"
            done
        fi
    else
        local pids=$(pgrep -f "$process_pattern" 2>/dev/null || true)
        if [[ -n "$pids" ]]; then
            echo "  PIDs: $pids"
            echo "  EN:"
            echo "$pids" | while read pid; do
                ps -p "$pid" -o pid,ppid,etime,pcpu,pmem,cmd --no-headers 2>/dev/null | while read line; do
                    echo "    $line"
                done
            done
        fi
    fi
}

# =============================================================================
# CheckEN
# =============================================================================

check_redis() {
    log_header "Redis ServiceStatus"
    
    if redis-cli ping >/dev/null 2>&1; then
        log_success "Redis ServiceEN"
        
        # ENRedisEN
        echo -e "\n${CYAN}📊 Redis EN:${NC}"
        redis-cli info server | grep -E "(redis_version|uptime_in_seconds|connected_clients)" | while read line; do
            echo "  $line"
        done
        return 0
    else
        log_error "Redis ServiceEN"
        return 1
    fi
}

check_backend() {
    log_header "EN API ServiceStatus"
    
    # CheckENStatus
    if check_process_status "$BACKEND_PID_FILE" "ENService" "uvicorn.*backend.main:app"; then
        # CheckENStatus
        if check_service_health "http://localhost:$BACKEND_PORT/api/v1/health/" "ENAPI"; then
            get_service_info "ENService" "$BACKEND_PID_FILE" "uvicorn.*backend.main:app"
            return 0
        else
            log_warning "ENAPIEN"
            return 1
        fi
    else
        return 1
    fi
}

check_frontend() {
    log_header "ENServiceStatus"
    
    # CheckENStatus
    if check_process_status "$FRONTEND_PID_FILE" "ENService" "npm.*dev\|vite"; then
        # CheckENStatus
        if check_service_health "http://localhost:$FRONTEND_PORT/" "EN"; then
            get_service_info "ENService" "$FRONTEND_PID_FILE" "npm.*dev\|vite"
            return 0
        else
            log_warning "ENServiceEN"
            return 1
        fi
    else
        return 1
    fi
}

check_celery() {
    log_header "Celery Worker Status"
    
    # CheckENStatus
    if check_process_status "$CELERY_PID_FILE" "Celery Worker" "celery.*worker"; then
        get_service_info "Celery Worker" "$CELERY_PID_FILE" "celery.*worker"
        
        # CheckCeleryEN
        if command -v celery >/dev/null 2>&1; then
            echo -e "\n${CYAN}📊 Celery EN:${NC}"
            if PYTHONPATH="${PWD}:${PYTHONPATH:-}" celery -A backend.core.celery_app inspect active >/dev/null 2>&1; then
                log_success "Celery EN"
                
                # EN
                local active_tasks=$(PYTHONPATH="${PWD}:${PYTHONPATH:-}" celery -A backend.core.celery_app inspect active 2>/dev/null | jq -r '.[] | length' 2>/dev/null || echo "0")
                echo "  EN: $active_tasks"
            else
                log_warning "Celery ENTestFailed"
            fi
        fi
        return 0
    else
        return 1
    fi
}

check_database() {
    log_header "ENStatus"
    
    if [[ -f "data/autoclip.db" ]]; then
        log_success "EN"
        
        # EN
        echo -e "\n${CYAN}📊 EN:${NC}"
        local db_size=$(du -h "data/autoclip.db" 2>/dev/null | cut -f1)
        echo "  EN: $db_size"
        
        # CheckEN
        if python -c "
import sys
sys.path.insert(0, '.')
from backend.core.database import test_connection
if test_connection():
    print('EN')
else:
    print('ENFailed')
    sys.exit(1)
" 2>/dev/null; then
            log_success "EN"
        else
            log_error "ENFailed"
            return 1
        fi
    else
        log_warning "EN"
        return 1
    fi
}

check_logs() {
    log_header "ENStatus"
    
    if [[ -d "$LOG_DIR" ]]; then
        log_success "EN"
        
        echo -e "\n${CYAN}📊 EN:${NC}"
        ls -la "$LOG_DIR"/*.log 2>/dev/null | while read line; do
            echo "  $line"
        done
        
        # EN
        echo -e "\n${CYAN}📝 EN (EN10EN):${NC}"
        for log_file in "$LOG_DIR"/*.log; do
            if [[ -f "$log_file" ]]; then
                echo -e "\n${YELLOW}$(basename "$log_file"):${NC}"
                tail -n 5 "$log_file" 2>/dev/null | while read line; do
                    echo "  $line"
                done
            fi
        done
    else
        log_warning "EN"
    fi
}

# =============================================================================
# EN
# =============================================================================

main() {
    log_header "AutoClip SystemStatusCheck v2.0"
    
    local overall_status=0
    
    # CheckENService
    check_redis || overall_status=1
    check_database || overall_status=1
    check_celery || overall_status=1
    check_backend || overall_status=1
    check_frontend || overall_status=1
    check_logs
    
    # ENStatus
    log_header "SystemENStatus"
    
    if [[ $overall_status -eq 0 ]]; then
        log_success "AllServiceEN"
        echo ""
        echo -e "${WHITE}🎉 AutoClip SystemEN！${NC}"
        echo ""
        echo -e "${CYAN}🌐 EN:${NC}"
        echo -e "  EN: http://localhost:$FRONTEND_PORT"
        echo -e "  ENAPI:  http://localhost:$BACKEND_PORT"
        echo -e "  APIEN:  http://localhost:$BACKEND_PORT/docs"
    else
        log_error "ENServiceEN"
        echo ""
        echo -e "${YELLOW}💡 EN:${NC}"
        echo -e "  1. ENErrorEN"
        echo -e "  2. ENSystem: ./stop_autoclip.sh && ./start_autoclip.sh"
        echo -e "  3. CheckEnvironmentConfigENDependencies"
    fi
    
    echo ""
    echo -e "${CYAN}📋 EN:${NC}"
    echo -e "  StartSystem: ./start_autoclip.sh"
    echo -e "  StopSystem: ./stop_autoclip.sh"
    echo -e "  EN: tail -f $LOG_DIR/*.log"
}

# EN
main "$@"
