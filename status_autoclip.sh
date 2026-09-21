#!/bin/bash

# AutoClip Systemstatuschecktranslated
# version: 2.0
# feature: checkAutoClipSystemtranslatedservice'stranslatedstatus

set -euo pipefail

# =============================================================================
# configtranslated
# =============================================================================

# servicetranslatedconfig
BACKtranslatedD_PORT=8000
FRONTtranslatedD_PORT=3000
REDIS_PORT=6379

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
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# translated
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

# checkservicetranslatedstatus
check_service_health() {
    local url="$1"
    local service_name="$2"
    
    if curl -fsS "$url" >/dev/null 2>&1; then
        echo -e "${GREtranslated}${ICON_HEALTH} $service_name translated${NC}"
        return 0
    else
        echo -e "${RED}${ICON_SICK} $service_name translated${NC}"
        return 1
    fi
}

# checkprocessstatus
check_process_status() {
    local pid_file="$1"
    local service_name="$2"
    local process_pattern="$3"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "${GREtranslated}${ICON_SUCCESS} $service_name translated (PID: $pid)${NC}"
            return 0
        else
            echo -e "${RED}${ICON_ERROR} $service_name PIDfiletranslatedintranslatedprocessnot found${NC}"
            return 1
        fi
    else
        # checkIstranslatedprocessintranslated
        if pgrep -f "$process_pattern" >/dev/null; then
            local pids=$(pgrep -f "$process_pattern" | tr '\n' ' ')
            echo -e "${YELLOW}${ICON_WARNING} $service_name translatedPIDfile (PIDs: $pids)${NC}"
            return 0
        else
            echo -e "${RED}${ICON_ERROR} $service_name translated${NC}"
            return 1
        fi
    fi
}

# fetchserviceinfo
get_service_info() {
    local service_name="$1"
    local pid_file="$2"
    local process_pattern="$3"
    
    echo -e "\n${CYAN}📊 $service_name translatedinfo:${NC}"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo "  PID: $pid"
            echo "  processinfo:"
            ps -p "$pid" -o pid,ppid,etime,pcpu,pmem,cmd --no-headers 2>/dev/null | while read line; do
                echo "    $line"
            done
        fi
    else
        local pids=$(pgrep -f "$process_pattern" 2>/dev/null || true)
        if [[ -n "$pids" ]]; then
            echo "  PIDs: $pids"
            echo "  processinfo:"
            echo "$pids" | while read pid; do
                ps -p "$pid" -o pid,ppid,etime,pcpu,pmem,cmd --no-headers 2>/dev/null | while read line; do
                    echo "    $line"
                done
            done
        fi
    fi
}

# =============================================================================
# checktranslated
# =============================================================================

check_redis() {
    log_header "Redis servicestatus"
    
    if redis-cli ping >/dev/null 2>&1; then
        log_success "Redis servicetranslated"
        
        # fetchRedisinfo
        echo -e "\n${CYAN}📊 Redis translatedinfo:${NC}"
        redis-cli info server | grep -E "(redis_version|uptime_in_seconds|connected_clients)" | while read line; do
            echo "  $line"
        done
        return 0
    else
        log_error "Redis servicetranslatedortranslatedconnect"
        return 1
    fi
}

check_backend() {
    log_header "backend API servicestatus"
    
    # checkprocessstatus
    if check_process_status "$BACKtranslatedD_PID_FILE" "backendservice" "uvicorn.*backend.main:app"; then
        # checktranslatedstatus
        if check_service_health "http://localhost:$BACKtranslatedD_PORT/api/v1/health/" "backendAPI"; then
            get_service_info "backendservice" "$BACKtranslatedD_PID_FILE" "uvicorn.*backend.main:app"
            return 0
        else
            log_warning "backendprocesstranslatedAPItranslated"
            return 1
        fi
    else
        return 1
    fi
}

check_frontend() {
    log_header "frontendservicestatus"
    
    # checkprocessstatus
    if check_process_status "$FRONTtranslatedD_PID_FILE" "frontendservice" "npm.*dev\|vite"; then
        # checktranslatedstatus
        if check_service_health "http://localhost:$FRONTtranslatedD_PORT/" "frontendInterface"; then
            get_service_info "frontendservice" "$FRONTtranslatedD_PID_FILE" "npm.*dev\|vite"
            return 0
        else
            log_warning "frontendprocesstranslatedservicetranslated"
            return 1
        fi
    else
        return 1
    fi
}

check_celery() {
    log_header "Celery Worker status"
    
    # checkprocessstatus
    if check_process_status "$CELERY_PID_FILE" "Celery Worker" "celery.*worker"; then
        get_service_info "Celery Worker" "$CELERY_PID_FILE" "celery.*worker"
        
        # checkCeleryconnect
        if command -v celery >/dev/null 2>&1; then
            echo -e "\n${CYAN}📊 Celery translatedinfo:${NC}"
            if PYTHONPATH="${PWD}:${PYTHONPATH:-}" celery -A backend.core.celery_app inspect active >/dev/null 2>&1; then
                log_success "Celery connecttranslated"
                
                # fetchtranslatedtask
                local active_tasks=$(PYTHONPATH="${PWD}:${PYTHONPATH:-}" celery -A backend.core.celery_app inspect active 2>/dev/null | jq -r '.[] | length' 2>/dev/null || echo "0")
                echo "  translatedtasktranslated: $active_tasks"
            else
                log_warning "Celery connecttestfailed"
            fi
        fi
        return 0
    else
        return 1
    fi
}

check_database() {
    log_header "databasestatus"
    
    if [[ -f "data/autoclip.db" ]]; then
        log_success "databasefiletranslatedin"
        
        # fetchdatabaseinfo
        echo -e "\n${CYAN}📊 databasetranslatedinfo:${NC}"
        local db_size=$(du -h "data/autoclip.db" 2>/dev/null | cut -f1)
        echo "  filetranslated: $db_size"
        
        # checkdatabaseconnect
        if python -c "
import sys
sys.path.insert(0, '.')
from backend.core.database import test_connection
if test_connection():
    print('databaseconnecttranslated')
else:
    print('databaseconnectfailed')
    sys.exit(1)
" 2>/dev/null; then
            log_success "databaseconnecttranslated"
        else
            log_error "databaseconnectfailed"
            return 1
        fi
    else
        log_warning "databasefile not found"
        return 1
    fi
}

check_logs() {
    log_header "logsfilestatus"
    
    if [[ -d "$LOG_DIR" ]]; then
        log_success "logsdirectorytranslatedin"
        
        echo -e "\n${CYAN}📊 logsfileinfo:${NC}"
        ls -la "$LOG_DIR"/*.log 2>/dev/null | while read line; do
            echo "  $line"
        done
        
        # translatedlogs
        echo -e "\n${CYAN}📝 translatedlogs (translated10translated):${NC}"
        for log_file in "$LOG_DIR"/*.log; do
            if [[ -f "$log_file" ]]; then
                echo -e "\n${YELLOW}$(basename "$log_file"):${NC}"
                tail -n 5 "$log_file" 2>/dev/null | while read line; do
                    echo "  $line"
                done
            fi
        done
    else
        log_warning "logsdirectorynot found"
    fi
}

# =============================================================================
# translated
# =============================================================================

main() {
    log_header "AutoClip Systemstatuscheck v2.0"
    
    local overall_status=0
    
    # checktranslated service
    check_redis || overall_status=1
    check_database || overall_status=1
    check_celery || overall_status=1
    check_backend || overall_status=1
    check_frontend || overall_status=1
    check_logs
    
    # translatedstatus
    log_header "Systemtranslatedstatus"
    
    if [[ $overall_status -eq 0 ]]; then
        log_success "translatedservicetranslated"
        echo ""
        echo -e "${WHITE}🎉 AutoClip Systemtranslated！${NC}"
        echo ""
        echo -e "${CYAN}🌐 translated:${NC}"
        echo -e "  frontendInterface: http://localhost:$FRONTtranslatedD_PORT"
        echo -e "  backendAPI:  http://localhost:$BACKtranslatedD_PORT"
        echo -e "  APIdocs:  http://localhost:$BACKtranslatedD_PORT/docs"
    else
        log_error "translatedservicetranslatedinissue"
        echo ""
        echo -e "${YELLOW}💡 translated:${NC}"
        echo -e "  1. translatedlogsfiletranslatederrorinfo"
        echo -e "  2. translatedSystem: ./stop_autoclip.sh && ./start_autoclip.sh"
        echo -e "  3. checktranslatedconfigAnddependencies"
    fi
    
    echo ""
    echo -e "${CYAN}📋 translatedusetranslated:${NC}"
    echo -e "  startSystem: ./start_autoclip.sh"
    echo -e "  translatedSystem: ./stop_autoclip.sh"
    echo -e "  translatedlogs: tail -f $LOG_DIR/*.log"
}

# translated
main "$@"
