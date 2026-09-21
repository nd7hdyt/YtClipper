#!/bin/bash

# AutoClip Docker StatusCheckScript
# Version: 1.0
# EN: CheckAutoClip DockerServiceStatus

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
ICON_HEALTH="💚"
ICON_SICK="🤒"
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
    log_header "DockerEnvironmentCheck"
    
    if ! command -v docker >/dev/null 2>&1; then
        log_error "DockerENInstall"
        return 1
    fi
    log_success "DockerENInstall"
    
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_error "Docker ComposeENInstall"
        return 1
    fi
    log_success "Docker ComposeENInstall"
    
    if ! docker info >/dev/null 2>&1; then
        log_error "DockerServiceEN"
        return 1
    fi
    log_success "DockerServiceEN"
    
    return 0
}

check_containers() {
    log_header "ENStatusCheck"
    
    local containers=$(docker ps -a --filter "name=autoclip" --format "{{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || true)
    
    if [[ -z "$containers" ]]; then
        log_warning "ENAutoClipEN"
        return 1
    fi
    
    echo -e "${CYAN}📊 ENStatus:${NC}"
    echo "$containers" | while IFS=$'\t' read -r name status ports; do
        if [[ "$status" == *"Up"* ]]; then
            echo -e "  ${GREEN}${ICON_HEALTH} $name${NC} - $status"
        else
            echo -e "  ${RED}${ICON_SICK} $name${NC} - $status"
        fi
    done
    
    return 0
}

check_services() {
    log_header "ServiceENCheck"
    
    # CheckENAPI
    if curl -fsS "http://localhost:8000/api/v1/health/" >/dev/null 2>&1; then
        log_success "ENAPIServiceEN"
    else
        log_error "ENAPIServiceEN"
    fi
    
    # CheckENService
    if curl -fsS "http://localhost:3000/" >/dev/null 2>&1; then
        log_success "ENServiceEN"
    else
        log_error "ENServiceEN"
    fi
    
    # CheckRedis
    if docker exec autoclip-redis redis-cli ping >/dev/null 2>&1; then
        log_success "RedisServiceEN"
    else
        log_error "RedisServiceEN"
    fi
}

check_volumes() {
    log_header "ENCheck"
    
    local volumes=$(docker volume ls --filter "name=autoclip" --format "{{.Name}}\t{{.Driver}}\t{{.Size}}" 2>/dev/null || true)
    
    if [[ -z "$volumes" ]]; then
        log_warning "ENAutoClipEN"
        return 1
    fi
    
    echo -e "${CYAN}💾 EN:${NC}"
    echo "$volumes" | while IFS=$'\t' read -r name driver size; do
        echo -e "  ${ICON_INFO} $name ($driver) - $size"
    done
    
    return 0
}

check_networks() {
    log_header "ENCheck"
    
    local networks=$(docker network ls --filter "name=autoclip" --format "{{.Name}}\t{{.Driver}}\t{{.Scope}}" 2>/dev/null || true)
    
    if [[ -z "$networks" ]]; then
        log_warning "ENAutoClipEN"
        return 1
    fi
    
    echo -e "${CYAN}🌐 EN:${NC}"
    echo "$networks" | while IFS=$'\t' read -r name driver scope; do
        echo -e "  ${ICON_INFO} $name ($driver) - $scope"
    done
    
    return 0
}

check_resources() {
    log_header "EN"
    
    echo -e "${CYAN}📊 EN:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}" $(docker ps --filter "name=autoclip" --format "{{.Names}}" 2>/dev/null || true) 2>/dev/null || log_warning "EN"
}

show_access_info() {
    log_header "EN"
    
    echo -e "${CYAN}🌐 ServiceEN:${NC}"
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
    log_header "AutoClip Docker StatusCheck v1.0"
    
    local overall_status=0
    
    # CheckDockerEnvironment
    if ! check_docker; then
        overall_status=1
    fi
    
    # CheckENStatus
    if ! check_containers; then
        overall_status=1
    fi
    
    # CheckServiceENStatus
    check_services
    
    # CheckEN
    check_volumes
    
    # CheckEN
    check_networks
    
    # CheckEN
    check_resources
    
    # EN
    show_access_info
    
    # ENStatus
    log_header "ENStatus"
    
    if [[ $overall_status -eq 0 ]]; then
        log_success "AutoClip DockerServiceEN"
        echo -e "\n${WHITE}🎉 AllServiceEN！${NC}"
    else
        log_error "ENServiceEN"
        echo -e "\n${YELLOW}💡 EN:${NC}"
        echo -e "  1. EN: docker-compose logs"
        echo -e "  2. ENService: docker-compose restart"
        echo -e "  3. ENStart: ./docker-start.sh"
    fi
}

# EN
show_help() {
    echo "AutoClip Docker StatusCheckScript"
    echo ""
    echo "EN:"
    echo "  $0 [EN]"
    echo ""
    echo "EN:"
    echo "  help    EN"
    echo ""
    echo "EN:"
    echo "  $0          # CheckServiceStatus"
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
