#!/bin/bash

# AutoClip Docker statuschecktranslated
# version: 1.0
# feature: checkAutoClip Dockerservicestatus

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
ICON_HEALTH="💚"
ICON_SICK="🤒"
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
    log_header "Dockertranslatedcheck"
    
    if ! command -v docker >/dev/null 2>&1; then
        log_error "Dockertranslatedinstall"
        return 1
    fi
    log_success "Dockertranslatedinstall"
    
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_error "Docker Composetranslatedinstall"
        return 1
    fi
    log_success "Docker Composetranslatedinstall"
    
    if ! docker info >/dev/null 2>&1; then
        log_error "Dockerservicetranslated"
        return 1
    fi
    log_success "Dockerservicetranslated"
    
    return 0
}

check_containers() {
    log_header "translatedstatuscheck"
    
    local containers=$(docker ps -a --filter "name=autoclip" --format "{{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || true)
    
    if [[ -z "$containers" ]]; then
        log_warning "translatedAutoCliptranslated"
        return 1
    fi
    
    echo -e "${CYAN}📊 translatedstatus:${NC}"
    echo "$containers" | while IFS=$'\t' read -r name status ports; do
        if [[ "$status" == *"Up"* ]]; then
            echo -e "  ${GREtranslated}${ICON_HEALTH} $name${NC} - $status"
        else
            echo -e "  ${RED}${ICON_SICK} $name${NC} - $status"
        fi
    done
    
    return 0
}

check_services() {
    log_header "serviceHealth Check"
    
    # checkbackendAPI
    if curl -fsS "http://localhost:8000/api/v1/health/" >/dev/null 2>&1; then
        log_success "backendAPIservicetranslated"
    else
        log_error "backendAPIservicetranslated"
    fi
    
    # checkfrontendservice
    if curl -fsS "http://localhost:3000/" >/dev/null 2>&1; then
        log_success "frontendservicetranslated"
    else
        log_error "frontendservicetranslated"
    fi
    
    # checkRedis
    if docker exec autoclip-redis redis-cli ping >/dev/null 2>&1; then
        log_success "Redisservicetranslated"
    else
        log_error "Redisservicetranslated"
    fi
}

check_volumes() {
    log_header "translatedcheck"
    
    local volumes=$(docker volume ls --filter "name=autoclip" --format "{{.Name}}\t{{.Driver}}\t{{.Size}}" 2>/dev/null || true)
    
    if [[ -z "$volumes" ]]; then
        log_warning "translatedAutoCliptranslated"
        return 1
    fi
    
    echo -e "${CYAN}💾 translated:${NC}"
    echo "$volumes" | while IFS=$'\t' read -r name driver size; do
        echo -e "  ${ICON_INFO} $name ($driver) - $size"
    done
    
    return 0
}

check_networks() {
    log_header "translatedcheck"
    
    local networks=$(docker network ls --filter "name=autoclip" --format "{{.Name}}\t{{.Driver}}\t{{.Scope}}" 2>/dev/null || true)
    
    if [[ -z "$networks" ]]; then
        log_warning "translatedAutoCliptranslated"
        return 1
    fi
    
    echo -e "${CYAN}🌐 translated:${NC}"
    echo "$networks" | while IFS=$'\t' read -r name driver scope; do
        echo -e "  ${ICON_INFO} $name ($driver) - $scope"
    done
    
    return 0
}

check_resources() {
    log_header "translatedusetranslated"
    
    echo -e "${CYAN}📊 translateduse:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}" $(docker ps --filter "name=autoclip" --format "{{.Names}}" 2>/dev/null || true) 2>/dev/null || log_warning "translatedfetchtranslatedusetranslated"
}

show_access_info() {
    log_header "translatedinfo"
    
    echo -e "${CYAN}🌐 servicetranslated:${NC}"
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
    log_header "AutoClip Docker statuscheck v1.0"
    
    local overall_status=0
    
    # checkDockertranslated
    if ! check_docker; then
        overall_status=1
    fi
    
    # checktranslatedstatus
    if ! check_containers; then
        overall_status=1
    fi
    
    # checkservicetranslatedstatus
    check_services
    
    # checktranslated
    check_volumes
    
    # checktranslated
    check_networks
    
    # checktranslateduse
    check_resources
    
    # translatedinfo
    show_access_info
    
    # translatedstatus
    log_header "translatedstatus"
    
    if [[ $overall_status -eq 0 ]]; then
        log_success "AutoClip Dockerservicetranslated"
        echo -e "\n${WHITE}🎉 translatedservicetranslated！${NC}"
    else
        log_error "translatedservicetranslatedinissue"
        echo -e "\n${YELLOW}💡 translated:${NC}"
        echo -e "  1. translatedlogs: docker-compose logs"
        echo -e "  2. translatedservice: docker-compose restart"
        echo -e "  3. translatedstart: ./docker-start.sh"
    fi
}

# translatedinfo
show_help() {
    echo "AutoClip Docker statuschecktranslated"
    echo ""
    echo "usetranslated:"
    echo "  $0 [Selecttranslated]"
    echo ""
    echo "Selecttranslated:"
    echo "  help    translatedinfo"
    echo ""
    echo "translated:"
    echo "  $0          # checkservicestatus"
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
