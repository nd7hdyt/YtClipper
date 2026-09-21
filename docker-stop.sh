#!/bin/bash

# AutoClip Docker StopScript
# Version: 1.0
# EN: StopAutoClip DockerService

set -euo pipefail

# =============================================================================
# ConfigEN
# =============================================================================

# EN
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

# =============================================================================
# StopEN
# =============================================================================

stop_services() {
    log_header "StopAutoClipService"
    
    local mode="${1:-production}"
    local compose_file="docker-compose.yml"
    
    if [[ "$mode" == "dev" ]]; then
        compose_file="docker-compose.dev.yml"
    fi
    
    log_info "StopService (EN: $mode)..."
    
    # StopService
    if docker-compose -f "$compose_file" down; then
        log_success "ServiceENStop"
    else
        log_error "StopServiceFailed"
        exit 1
    fi
}

cleanup_containers() {
    log_header "EN"
    
    # StopAllEN
    local containers=$(docker ps -a --filter "name=autoclip" --format "{{.Names}}" 2>/dev/null || true)
    
    if [[ -n "$containers" ]]; then
        log_info "ENAutoClipEN:"
        echo "$containers"
        
        if [[ "${1:-}" == "--force" ]]; then
            log_info "ENStopAllEN..."
            echo "$containers" | xargs docker stop 2>/dev/null || true
            echo "$containers" | xargs docker rm 2>/dev/null || true
            log_success "ENCompleted"
        else
            log_warning "EN --force EN"
        fi
    else
        log_success "ENAutoClipEN"
    fi
}

cleanup_images() {
    log_header "EN"
    
    if [[ "${1:-}" == "--force" ]]; then
        log_info "EN..."
        docker image prune -f
        log_success "ENCompleted"
    else
        log_info "EN --force EN"
    fi
}

cleanup_volumes() {
    log_header "EN"
    
    if [[ "${1:-}" == "--force" ]]; then
        log_warning "ENAllEN，ENProjectEN！"
        read -p "EN？(y/N): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "EN..."
            docker volume prune -f
            log_success "ENCompleted"
        else
            log_info "EN"
        fi
    else
        log_info "EN --force EN"
    fi
}

show_status() {
    log_header "CurrentStatus"
    
    echo -e "${BLUE}📊 ENStatus:${NC}"
    docker-compose ps 2>/dev/null || echo "  ENService"
    
    echo -e "\n${BLUE}🐳 AutoClipEN:${NC}"
    docker ps -a --filter "name=autoclip" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "  EN"
    
    echo -e "\n${BLUE}💾 EN:${NC}"
    docker volume ls --filter "name=autoclip" --format "table {{.Name}}\t{{.Driver}}\t{{.Size}}" 2>/dev/null || echo "  EN"
}

# =============================================================================
# EN
# =============================================================================

main() {
    local mode="production"
    local cleanup=false
    local force=false
    
    # EN
    while [[ $# -gt 0 ]]; do
        case $1 in
            "dev")
                mode="development"
                shift
                ;;
            "--cleanup")
                cleanup=true
                shift
                ;;
            "--force")
                force=true
                shift
                ;;
            "help"|"-h"|"--help")
                show_help
                exit 0
                ;;
            *)
                log_error "EN: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    log_header "AutoClip Docker StopEN v1.0"
    
    # StopService
    stop_services "$mode"
    
    # EN（IfNeed）
    if [[ "$cleanup" == true ]]; then
        cleanup_containers "$force"
        cleanup_images "$force"
        cleanup_volumes "$force"
    fi
    
    # ENStatus
    show_status
    
    echo -e "\n${GREEN}🎉 AutoClip Docker ServiceENStop${NC}"
}

# EN
show_help() {
    echo "AutoClip Docker StopScript"
    echo ""
    echo "EN:"
    echo "  $0 [EN]"
    echo ""
    echo "EN:"
    echo "  dev          StopENEnvironment"
    echo "  --cleanup    StopEN"
    echo "  --force      EN（EN）"
    echo "  help         EN"
    echo ""
    echo "EN:"
    echo "  $0                    # StopENEnvironment"
    echo "  $0 dev                # StopENEnvironment"
    echo "  $0 --cleanup          # StopEN"
    echo "  $0 --cleanup --force  # StopENAllEN"
    echo "  $0 help               # EN"
    echo ""
    echo "EN:"
    echo "  --force ENAllEN，PleaseEN！"
}

# EN
main "$@"
