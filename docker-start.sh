#!/bin/bash

# AutoClip Docker starttranslated
# version: 1.0
# feature: useDockertranslatedstartAutoClipSystem

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
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# translated
ICON_SUCCESS="✅"
ICON_ERROR="❌"
ICON_WARNING="⚠️"
ICON_INFO="ℹ️"
ICON_ROCKET="🚀"
ICON_DOCKER="🐳"

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

# =============================================================================
# checktranslated
# =============================================================================

check_docker() {
    log_header "checkDockertranslated"
    
    if ! command -v docker >/dev/null 2>&1; then
        log_error "Dockertranslatedinstall，translatedinstallDocker"
        exit 1
    fi
    log_success "Dockertranslatedinstall"
    
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_error "Docker Composetranslatedinstall，translatedinstallDocker Compose"
        exit 1
    fi
    log_success "Docker Composetranslatedinstall"
    
    if ! docker info >/dev/null 2>&1; then
        log_error "Dockerservicetranslated，translatedstartDockerservice"
        exit 1
    fi
    log_success "Dockerservicetranslated"
}

check_environment() {
    log_header "checktranslatedconfig"
    
    if [[ ! -f ".env" ]]; then
        log_warning ".envfile not found，createdefaultconfig..."
        if [[ -f "env.example" ]]; then
            cp env.example .env
            log_success "translatedcreatedefault.envfile"
            log_warning "translated.envfile，translated'sconfig（translatedIsAPIkey）"
        else
            log_error "env.examplefile not found"
            exit 1
        fi
    else
        log_success ".envfiletranslatedin"
    fi
    
    # checktranslated'sconfig
    if ! grep -q "API_DASHSCOPE_API_KEY" .env || grep -q "API_DASHSCOPE_API_KEY=$" .env; then
        log_warning "API_DASHSCOPE_API_KEYtranslatedconfig，AIfeaturetranslatedcanuse"
    fi
}

check_ports() {
    log_header "checktranslateduse"
    
    local ports=(8000 3000 6379 5555)
    local occupied_ports=()
    
    for port in "${ports[@]}"; do
        if lsof -i ":$port" >/dev/null 2>&1; then
            occupied_ports+=("$port")
        fi
    done
    
    if [[ ${#occupied_ports[@]} -gt 0 ]]; then
        log_warning "translateduse: ${occupied_ports[*]}"
        log_info "Dockertranslatedprocesstranslated，translatedusethistranslated'sservice"
    else
        log_success "translatedcanuse"
    fi
}

# =============================================================================
# starttranslated
# =============================================================================

start_services() {
    log_header "startAutoClipservice"
    
    # Selectselectstarttranslated
    if [[ "${1:-}" == "dev" ]]; then
        log_info "starttranslated..."
        docker-compose -f docker-compose.dev.yml up -d
        COMPOSE_FILE="docker-compose.dev.yml"
    else
        log_info "starttranslated..."
        docker-compose up -d
        COMPOSE_FILE="docker-compose.yml"
    fi
    
    # etc.translatedservicestart
    log_info "etc.translatedservicestart..."
    sleep 10
    
    # checkservicestatus
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        log_success "servicestartsucceeded"
    else
        log_error "servicestartfailed"
        log_info "translatedlogs: docker-compose -f $COMPOSE_FILE logs"
        exit 1
    fi
}

show_status() {
    log_header "servicestatus"
    
    echo -e "${CYAN}📊 translatedstatus:${NC}"
    docker-compose ps
    
    echo -e "\n${CYAN}🌐 translated:${NC}"
    echo -e "  frontendInterface: http://localhost:3000"
    echo -e "  backendAPI:  http://localhost:8000"
    echo -e "  APIdocs:  http://localhost:8000/docs"
    echo -e "  Flowermonitor: http://localhost:5555"
    
    echo -e "\n${CYAN}📝 translatedusetranslated:${NC}"
    echo -e "  translatedlogs: docker-compose logs -f"
    echo -e "  translatedservice: docker-compose down"
    echo -e "  translatedservice: docker-compose restart"
    echo -e "  translated: docker-compose exec autoclip bash"
}

# =============================================================================
# translated
# =============================================================================

main() {
    log_header "AutoClip Docker starttranslated v1.0"
    
    # translated
    local mode="production"
    if [[ "${1:-}" == "dev" ]]; then
        mode="development"
    fi
    
    log_info "starttranslated: $mode"
    
    # translatedcheck
    check_docker
    check_environment
    check_ports
    
    # startservice
    start_services "$mode"
    
    # translatedstatus
    show_status
    
    echo -e "\n${WHITE}🎉 AutoClip Docker translated！${NC}"
    echo -e "${YELLOW}💡 translated: translatedstartcantranslatedminutestranslateddownloadAndtranslated${NC}"
}

# translatedinfo
show_help() {
    echo "AutoClip Docker starttranslated"
    echo ""
    echo "usetranslated:"
    echo "  $0 [Selecttranslated]"
    echo ""
    echo "Selecttranslated:"
    echo "  dev     starttranslated"
    echo "  help    translatedinfo"
    echo ""
    echo "translated:"
    echo "  $0          # starttranslated"
    echo "  $0 dev      # starttranslated"
    echo "  $0 help     # translated"
}

# processtranslated
case "${1:-}" in
    "help"|"-h"|"--help")
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
