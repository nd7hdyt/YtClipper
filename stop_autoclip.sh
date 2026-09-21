#!/bin/bash

# AutoClip SystemStopScript
# Version: 2.0
# EN: ENStopAllAutoClipService

set -euo pipefail

# =============================================================================
# ConfigEN
# =============================================================================

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
NC='\033[0m' # No Color

# EN
ICON_SUCCESS="✅"
ICON_ERROR="❌"
ICON_WARNING="⚠️"
ICON_INFO="ℹ️"
ICON_STOP="🛑"
ICON_CLEAN="🧹"

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
    echo -e "\n${PURPLE}${ICON_STOP} $1${NC}"
    echo -e "${PURPLE}$(printf '=%.0s' {1..50})${NC}"
}

# StopEN
stop_process() {
    local pid_file="$1"
    local service_name="$2"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            log_info "Stop $service_name (PID: $pid)..."
            
            # ENStop
            kill "$pid" 2>/dev/null || true
            
            # EN
            local count=0
            while kill -0 "$pid" 2>/dev/null && [[ $count -lt 10 ]]; do
                sleep 1
                ((count++))
            done
            
            # IfEN，ENStop
            if kill -0 "$pid" 2>/dev/null; then
                log_warning "ENStop $service_name..."
                kill -9 "$pid" 2>/dev/null || true
                sleep 1
            fi
            
            if kill -0 "$pid" 2>/dev/null; then
                log_error "ENStop $service_name"
            else
                log_success "$service_name ENStop"
            fi
        else
            log_warning "$service_name EN"
        fi
        rm -f "$pid_file"
    else
        log_info "$service_name PIDEN"
    fi
}

# StopAllEN
stop_all_processes() {
    log_header "StopAllAutoClipService"
    
    # StopENPIDEN
    stop_process "$BACKEND_PID_FILE" "ENService"
    stop_process "$FRONTEND_PID_FILE" "ENService"
    stop_process "$CELERY_PID_FILE" "Celery Worker"
    
    # StopAllEN
    log_info "StopAllCelery WorkerEN..."
    pkill -f "celery.*worker" 2>/dev/null || true
    
    log_info "StopAllENAPIEN..."
    pkill -f "uvicorn.*backend.main:app" 2>/dev/null || true
    
    log_info "StopAllENServiceEN..."
    pkill -f "npm.*dev" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    
    # ENStop
    sleep 2
    
    log_success "AllServiceENStop"
}

# EN
cleanup_temp_files() {
    log_header "EN"
    
    # ENPIDEN
    rm -f "$BACKEND_PID_FILE" "$FRONTEND_PID_FILE" "$CELERY_PID_FILE"
    log_success "PIDEN"
    
    # ENCeleryEN
    rm -f /tmp/celerybeat-schedule /tmp/celerybeat.pid 2>/dev/null || true
    log_success "CeleryEN"
    
    # ENPythonEN
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    log_success "PythonEN"
}

# ENSystemStatus
show_system_status() {
    log_header "SystemStatusCheck"
    
    local services_running=false
    
    # CheckENService
    if pgrep -f "uvicorn.*backend.main:app" >/dev/null; then
        log_warning "ENServiceEN"
        services_running=true
    else
        log_success "ENServiceENStop"
    fi
    
    # CheckENService
    if pgrep -f "npm.*dev\|vite" >/dev/null; then
        log_warning "ENServiceEN"
        services_running=true
    else
        log_success "ENServiceENStop"
    fi
    
    # CheckCelery Worker
    if pgrep -f "celery.*worker" >/dev/null; then
        log_warning "Celery WorkerEN"
        services_running=true
    else
        log_success "Celery WorkerENStop"
    fi
    
    if [[ "$services_running" == true ]]; then
        log_warning "ENServiceEN，ENNeedManualStop"
        echo ""
        echo "EN:"
        pgrep -f "uvicorn.*backend.main:app\|npm.*dev\|vite\|celery.*worker" | while read pid; do
            ps -p "$pid" -o pid,ppid,cmd --no-headers 2>/dev/null || true
        done
    else
        log_success "AllAutoClipServiceENStop"
    fi
}

# EN
show_log_info() {
    log_header "EN"
    
    if [[ -d "$LOG_DIR" ]]; then
        echo "EN:"
        ls -la "$LOG_DIR"/*.log 2>/dev/null | while read line; do
            echo "  $line"
        done
        echo ""
        echo "EN:"
        echo "  EN: tail -f $LOG_DIR/backend.log"
        echo "  EN: tail -f $LOG_DIR/frontend.log"
        echo "  CeleryEN: tail -f $LOG_DIR/celery.log"
    else
        log_info "EN"
    fi
}

# =============================================================================
# EN
# =============================================================================

main() {
    log_header "AutoClip SystemStopEN v2.0"
    
    # StopAllService
    stop_all_processes
    
    # EN
    cleanup_temp_files
    
    # ENSystemStatus
    show_system_status
    
    # EN
    show_log_info
    
    echo ""
    log_success "AutoClip SystemENStop"
    echo ""
    echo "ENStart，PleaseEN: ./start_autoclip.sh"
}

# EN
main "$@"
