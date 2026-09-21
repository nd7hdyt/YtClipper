#!/bin/bash

# WhisperENStatusCheckScript
# ENCheckSystemStatus

echo "🔍 AutoClip WhisperENStatusCheck"
echo "=================================="

# CheckWhisperEN
echo "📊 WhisperENStatus:"
python scripts/monitor_whisper.py

echo ""
echo "📈 SystemEN:"
echo "CPUEN: $(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')"
echo "EN: $(ps -A -o %mem | awk '{s+=$1} END {print s "%"}')"

echo ""
echo "🛠️ EN:"
echo "  CheckStatus: python scripts/monitor_whisper.py"
echo "  EN: python scripts/monitor_whisper.py --kill-duplicates"
echo "  StopSystem: ./stop_autoclip.sh"
