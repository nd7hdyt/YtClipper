#!/bin/bash

# AutoClip Docker translated
# version: 1.0
# feature: translatedAutoClip Dockerservice

set -euo pipefail

# =============================================================================
# configtranslated
# =============================================================================

# translated
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

# =============================================================================
# translated
# =============================================================================

stop_services() {
    log_header "translatedAutoClipservice"
    
    local mode="${1:-production}"
    local compose_file="docker-compose.yml"
    
    if [[ "$mode" == "dev" ]]; then
        compose_file="docker-compose.dev.yml"
    fi
    
    log_info "translatedservice (translated: $mode)..."
    
    # translatedservice
    if docker-compose -f "$compose_file" down; then
        log_success "servicetranslated"
    else
        log_error "translatedservicefailed"
        exit 1
    fi
}

cleanup_containers() {
    log_header "cleantranslated"
    
    # translated
    local containers=$(docker ps -a --filter "name=autoclip" --format "{{.Names}}" 2>/dev/null || true)
    
    if [[ -n "$containers" ]]; then
        log_info "translatedAutoCliptranslated:"
        echo "$containers"
        
        if [[ "${1:-}" == "--force" ]]; then
            log_info "translated..."
            echo "$containers" | xargs docker stop 2>/dev/null || true
            echo "$containers" | xargs docker rm 2>/dev/null || true
            log_success "translatedcleantranslated"
        else
            log_warning "use --force translatedcleantranslated"
        fi
    else
        log_success "translatedAutoCliptranslated"
    fi
}

cleanup_images() {
    log_header "cleantranslated"
    
    if [[ "${1:-}" == "--force" ]]; then
        log_info "cleantranslateduse'stranslated..."
        docker image prune -f
        log_success "translatedcleantranslated"
    else
        log_info "use --force translatedcleantranslateduse'stranslated"
    fi
}

cleanup_volumes() {
    log_header "cleantranslated"
    
    if [[ "${1:-}" == "--force" ]]; then
        log_warning "thistranslateddeletetranslated，PackagetranslatedprojectfileAnddatabase！"
        read -p "translated？(y/N): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "cleantranslated..."
            docker volume prune -f
            log_success "translatedcleantranslated"
        else
            log_info "cancelcleantranslated"
        fi
    else
        log_info "use --force translatedcleantranslateduse'stranslated"
    fi
}

show_status() {
    log_header "translatedstatus"
    
    echo -e "${BLUE}📊 translatedstatus:${NC}"
    docker-compose ps 2>/dev/null || echo "  translated'sservice"
    
    echo -e "\n${BLUE}🐳 AutoCliptranslated:${NC}"
    docker ps -a --filter "name=autoclip" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "  translated"
    
    echo -e "\n${BLUE}💾 translated:${NC}"
    docker volume ls --filter "name=autoclip" --format "table {{.Name}}\t{{.Driver}}\t{{.Size}}" 2>/dev/null || echo "  translated"
}

# =============================================================================
# translated
# =============================================================================

main() {
    local mode="production"
    local cleanup=false
    local force=false
    
    # translated
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
                log_error "translated: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    log_header "AutoClip Docker translated v1.0"
    
    # translatedservice
    stop_services "$mode"
    
    # clean（iftranslated）
    if [[ "$cleanup" == true ]]; then
        cleanup_containers "$force"
        cleanup_images "$force"
        cleanup_volumes "$force"
    fi
    
    # translatedstatus
    show_status
    
    echo -e "\n${GREtranslated}🎉 AutoClip Docker servicetranslated${NC}"
}

# translatedinfo
show_help() {
    echo "AutoClip Docker translated"
    echo ""
    echo "usetranslated:"
    echo "  $0 [Selecttranslated]"
    echo ""
    echo "Selecttranslated:"
    echo "  dev          translated"
    echo "  --cleanup    translatedcleantranslated"
    echo "  --force      translatedclean（Packagetranslated）"
    echo "  help         translatedinfo"
    echo ""
    echo "translated:"
    echo "  $0                    # translated"
    echo "  $0 dev                # translated"
    echo "  $0 --cleanup          # translatedcleantranslated"
    echo "  $0 --cleanup --force  # translatedcleantranslated"
    echo "  $0 help               # translated"
    echo ""
    echo "translated:"
    echo "  --force translateddeletetranslated，translateduse！"
}

# translated
main "$@"
