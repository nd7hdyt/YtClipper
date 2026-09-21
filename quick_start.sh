#!/bin/bash

# AutoClip translatedstarttranslated
# version: 2.0
# feature: translatedstarttranslated，skiptranslatedcheck

set -euo pipefail

# =============================================================================
# configtranslated
# =============================================================================

BACKtranslatedD_PORT=8000
FRONTtranslatedD_PORT=3000

# =============================================================================
# translated
# =============================================================================

GREtranslated='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# =============================================================================
# tooltranslated
# =============================================================================

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREtranslated}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# =============================================================================
# translated
# =============================================================================

main() {
    echo -e "${GREtranslated}🚀 AutoClip translatedstart${NC}"
    echo ""
    
    # checktranslated
    if [[ ! -d "venv" ]]; then
        log_warning "translatednot found，translated: python3 -m venv venv"
        exit 1
    fi
    
    # translated
    log_info "translated..."
    source venv/bin/activate
    
    # settingsPythonpath
    : "${PYTHONPATH:=}"
    export PYTHONPATH="${PWD}:${PYTHONPATH}"
    
    # translated
    if [[ -f ".env" ]]; then
        set -a
        source .env
        set +a
    fi
    
    # startRedis（iftranslated）
    if ! redis-cli ping >/dev/null 2>&1; then
        log_info "startRedis..."
        if command -v brew >/dev/null; then
            brew services start redis
            sleep 2
        fi
    fi
    
    # createlogsdirectory
    mkdir -p logs
    
    # startbackend
    log_info "startbackendservice..."
    nohup python -m uvicorn backend.main:app --host 0.0.0.0 --port "$BACKtranslatedD_PORT" --reload > logs/backend.log 2>&1 &
    echo $! > backend.pid
    
    # startCelery Worker
    log_info "startCelery Worker..."
    nohup celery -A backend.core.celery_app worker --loglevel=info --concurrency=1 --prefetch-multiplier=1 -Q celery,processing,video,notification,upload > logs/celery.log 2>&1 &
    echo $! > celery.pid
    
    # startfrontend
    log_info "startfrontendservice..."
    cd frontend
    nohup npm run dev -- --host 0.0.0.0 --port "$FRONTtranslatedD_PORT" > ../logs/frontend.log 2>&1 &
    echo $! > ../frontend.pid
    cd ..
    
    # etc.translatedservicestart
    log_info "etc.translatedservicestart..."
    sleep 5
    
    # checkservicestatus
    if curl -fsS "http://localhost:$BACKtranslatedD_PORT/api/v1/health/" >/dev/null 2>&1; then
        log_success "backendservicetranslatedstart"
    else
        log_warning "backendservicestartcantranslatedissue"
    fi
    
    if curl -fsS "http://localhost:$FRONTtranslatedD_PORT/" >/dev/null 2>&1; then
        log_success "frontendservicetranslatedstart"
    else
        log_warning "frontendservicestartcantranslatedissue"
    fi
    
    echo ""
    log_success "translatedstarttranslated！"
    echo ""
    echo "🌐 translated:"
    echo "  frontend: http://localhost:$FRONTtranslatedD_PORT"
    echo "  backend: http://localhost:$BACKtranslatedD_PORT"
    echo "  APIdocs: http://localhost:$BACKtranslatedD_PORT/docs"
    echo ""
    echo "📝 translatedlogs:"
    echo "  tail -f logs/backend.log"
    echo "  tail -f logs/frontend.log"
    echo "  tail -f logs/celery.log"
    echo ""
    echo "🛑 translatedservice: ./stop_autoclip.sh"
}

# translated
main "$@"
