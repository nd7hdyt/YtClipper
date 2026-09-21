#!/bin/bash

# AutoClip Systemtranslated
# version: 2.0
# feature: translatedAutoClipservice

set -euo pipefail

# =============================================================================
# configtranslated
# =============================================================================

# PIDfile
BACKtranslatedD_PID_FILE="backend.pid"
FRONTtranslatedD_PID_FILE="frontend.pid"
CELERY_PID_FILE="celery.pid"

# logsdirectory
LOG_DIR="logs"

# =============================================================================
# translatedAndtranslated
# =============================================================================

RED='\033[0;31m'
GREtranslated='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# translated
ICON_SUCCESS="✅"
ICON_ERROR="❌"
ICON_WARNING="⚠️"
ICON_INFO="ℹ️"
ICON_STOP="🛑"
ICON_CLEAN="🧹"

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
    echo -e "\n${PURPLE}${ICON_STOP} $1${NC}"
    echo -e "${PURPLE}$(printf '=%.0s' {1..50})${NC}"
}

# translatedprocess
stop_process() {
    local pid_file="$1"
    local service_name="$2"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            log_info "translated $service_name (PID: $pid)..."
            
            # translated
            kill "$pid" 2>/dev/null || true
            
            # etc.translatedprocesstranslated
            local count=0
            while kill -0 "$pid" 2>/dev/null && [[ $count -lt 10 ]]; do
                sleep 1
                ((count++))
            done
            
            # iftranslatedprocesstranslatedintranslated，translated
            if kill -0 "$pid" 2>/dev/null; then
                log_warning "translated $service_name..."
                kill -9 "$pid" 2>/dev/null || true
                sleep 1
            fi
            
            if kill -0 "$pid" 2>/dev/null; then
                log_error "translated $service_name"
            else
                log_success "$service_name translated"
            fi
        else
            log_warning "$service_name processnot found"
        fi
        rm -f "$pid_file"
    else
        log_info "$service_name PIDfile not found"
    fi
}

# translatedprocess
stop_all_processes() {
    log_header "translatedAutoClipservice"
    
    # translatedPIDfiletranslated'sprocess
    stop_process "$BACKtranslatedD_PID_FILE" "backendservice"
    stop_process "$FRONTtranslatedD_PID_FILE" "frontendservice"
    stop_process "$CELERY_PID_FILE" "Celery Worker"
    
    # translatedprocess
    log_info "translatedCelery Workerprocess..."
    pkill -f "celery.*worker" 2>/dev/null || true
    
    log_info "translatedbackendAPIprocess..."
    pkill -f "uvicorn.*backend.main:app" 2>/dev/null || true
    
    log_info "translatedfrontendtranslatedservicetranslated..."
    pkill -f "npm.*dev" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    
    # etc.translatedprocesstranslated
    sleep 2
    
    log_success "translatedservicetranslated"
}

# clean temp files
cleanup_temp_files() {
    log_header "clean temp files"
    
    # cleanPIDfile
    rm -f "$BACKtranslatedD_PID_FILE" "$FRONTtranslatedD_PID_FILE" "$CELERY_PID_FILE"
    log_success "PIDfiletranslatedclean"
    
    # cleanCelerytranslatedfile
    rm -f /tmp/celerybeat-schedule /tmp/celerybeat.pid 2>/dev/null || true
    log_success "Celerytranslatedfiletranslatedclean"
    
    # cleanPythoncache
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    log_success "Pythoncachetranslatedclean"
}

# translatedSystemstatus
show_system_status() {
    log_header "Systemstatuscheck"
    
    local services_running=false
    
    # checkbackendservice
    if pgrep -f "uvicorn.*backend.main:app" >/dev/null; then
        log_warning "backendservicetranslatedintranslated"
        services_running=true
    else
        log_success "backendservicetranslated"
    fi
    
    # checkfrontendservice
    if pgrep -f "npm.*dev\|vite" >/dev/null; then
        log_warning "frontendservicetranslatedintranslated"
        services_running=true
    else
        log_success "frontendservicetranslated"
    fi
    
    # checkCelery Worker
    if pgrep -f "celery.*worker" >/dev/null; then
        log_warning "Celery Workertranslatedintranslated"
        services_running=true
    else
        log_success "Celery Workertranslated"
    fi
    
    if [[ "$services_running" == true ]]; then
        log_warning "translatedservicetranslatedintranslated，cantranslated"
        echo ""
        echo "translatedintranslated'sprocess:"
        pgrep -f "uvicorn.*backend.main:app\|npm.*dev\|vite\|celery.*worker" | while read pid; do
            ps -p "$pid" -o pid,ppid,cmd --no-headers 2>/dev/null || true
        done
    else
        log_success "translatedAutoClipservicetranslated"
    fi
}

# translatedlogsinfo
show_log_info() {
    log_header "logsfileinfo"
    
    if [[ -d "$LOG_DIR" ]]; then
        echo "logsfiletranslated:"
        ls -la "$LOG_DIR"/*.log 2>/dev/null | while read line; do
            echo "  $line"
        done
        echo ""
        echo "translatedlogs:"
        echo "  backendlogs: tail -f $LOG_DIR/backend.log"
        echo "  frontendlogs: tail -f $LOG_DIR/frontend.log"
        echo "  Celerylogs: tail -f $LOG_DIR/celery.log"
    else
        log_info "logsdirectorynot found"
    fi
}

# =============================================================================
# translated
# =============================================================================

main() {
    log_header "AutoClip Systemtranslated v2.0"
    
    # translatedservice
    stop_all_processes
    
    # clean temp files
    cleanup_temp_files
    
    # translatedSystemstatus
    show_system_status
    
    # translatedlogsinfo
    show_log_info
    
    echo ""
    log_success "AutoClip Systemtranslated"
    echo ""
    echo "iftranslatedstart，translated: ./start_autoclip.sh"
}

# translated
main "$@"
