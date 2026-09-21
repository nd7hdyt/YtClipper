#!/bin/bash

# AutoClip Docker StartScript
# Version: 1.0
# EN: ENDockerENStartAutoClipSystem

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
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# EN
ICON_SUCCESS="✅"
ICON_ERROR="❌"
ICON_WARNING="⚠️"
ICON_INFO="ℹ️"
ICON_ROCKET="🚀"
ICON_DOCKER="🐳"

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

# =============================================================================
# CheckEN
# =============================================================================

check_docker() {
    log_header "CheckDockerEnvironment"
    
    if ! command -v docker >/dev/null 2>&1; then
        log_error "DockerENInstall，PleaseENInstallDocker"
        exit 1
    fi
    log_success "DockerENInstall"
    
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_error "Docker ComposeENInstall，PleaseENInstallDocker Compose"
        exit 1
    fi
    log_success "Docker ComposeENInstall"
    
    if ! docker info >/dev/null 2>&1; then
        log_error "DockerServiceEN，PleaseStartDockerService"
        exit 1
    fi
    log_success "DockerServiceEN"
}

check_environment() {
    log_header "CheckEnvironmentConfig"
    
    if [[ ! -f ".env" ]]; then
        log_warning ".envEN，ENConfig..."
        if [[ -f "env.example" ]]; then
            cp env.example .env
            log_success "EN.envEN"
            log_warning "PleaseEN.envEN，ENConfig（ENAPIEN）"
        else
            log_error "env.exampleEN"
            exit 1
        fi
    else
        log_success ".envEN"
    fi
    
    # CheckENConfig
    if ! grep -q "API_DASHSCOPE_API_KEY" .env || grep -q "API_DASHSCOPE_API_KEY=$" .env; then
        log_warning "API_DASHSCOPE_API_KEYENConfig，AIEN"
    fi
}

check_ports() {
    log_header "CheckEN"
    
    local ports=(8000 3000 6379 5555)
    local occupied_ports=()
    
    for port in "${ports[@]}"; do
        if lsof -i ":$port" >/dev/null 2>&1; then
            occupied_ports+=("$port")
        fi
    done
    
    if [[ ${#occupied_ports[@]} -gt 0 ]]; then
        log_warning "EN: ${occupied_ports[*]}"
        log_info "DockerENAutoProcessingEN，ENStopENService"
    else
        log_success "AllEN"
    fi
}

# =============================================================================
# StartEN
# =============================================================================

start_services() {
    log_header "StartAutoClipService"
    
    # ENStartEN
    if [[ "${1:-}" == "dev" ]]; then
        log_info "StartENEnvironment..."
        docker-compose -f docker-compose.dev.yml up -d
        COMPOSE_FILE="docker-compose.dev.yml"
    else
        log_info "StartENEnvironment..."
        docker-compose up -d
        COMPOSE_FILE="docker-compose.yml"
    fi
    
    # ENServiceStart
    log_info "ENServiceStart..."
    sleep 10
    
    # CheckServiceStatus
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        log_success "ServiceStartSuccess"
    else
        log_error "ServiceStartFailed"
        log_info "EN: docker-compose -f $COMPOSE_FILE logs"
        exit 1
    fi
}

show_status() {
    log_header "ServiceStatus"
    
    echo -e "${CYAN}📊 ENStatus:${NC}"
    docker-compose ps
    
    echo -e "\n${CYAN}🌐 EN:${NC}"
    echo -e "  EN: http://localhost:3000"
    echo -e "  ENAPI:  http://localhost:8000"
    echo -e "  APIEN:  http://localhost:8000/docs"
    echo -e "  FlowerEN: http://localhost:5555"
    
    echo -e "\n${CYAN}📝 EN:${NC}"
    echo -e "  EN: docker-compose logs -f"
    echo -e "  StopService: docker-compose down"
    echo -e "  ENService: docker-compose restart"
    echo -e "  EN: docker-compose exec autoclip bash"
}

# =============================================================================
# EN
# =============================================================================

main() {
    log_header "AutoClip Docker StartEN v1.0"
    
    # EN
    local mode="production"
    if [[ "${1:-}" == "dev" ]]; then
        mode="development"
    fi
    
    log_info "StartEN: $mode"
    
    # ENCheck
    check_docker
    check_environment
    check_ports
    
    # StartService
    start_services "$mode"
    
    # ENStatus
    show_status
    
    echo -e "\n${WHITE}🎉 AutoClip Docker ENCompleted！${NC}"
    echo -e "${YELLOW}💡 EN: ENStartENNeedENDownloadEN${NC}"
}

# EN
show_help() {
    echo "AutoClip Docker StartScript"
    echo ""
    echo "EN:"
    echo "  $0 [EN]"
    echo ""
    echo "EN:"
    echo "  dev     StartENEnvironment"
    echo "  help    EN"
    echo ""
    echo "EN:"
    echo "  $0          # StartENEnvironment"
    echo "  $0 dev      # StartENEnvironment"
    echo "  $0 help     # EN"
}

# ProcessingEN
case "${1:-}" in
    "help"|"-h"|"--help")
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
