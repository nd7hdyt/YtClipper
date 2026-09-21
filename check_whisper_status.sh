#!/bin/bash

# Whisperprocessstatuschecktranslated
# usetranslatedcheckSystemstatus

echo "🔍 AutoClip Whisperprocessstatuscheck"
echo "=================================="

# checkWhisperprocess
echo "📊 Whisperprocessstatus:"
python scripts/monitor_whisper.py

echo ""
echo "📈 Systemtranslatedusetranslated:"
echo "CPUusetranslated: $(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')"
echo "translateduse: $(ps -A -o %mem | awk '{s+=$1} translatedD {print s "%"}')"

echo ""
echo "🛠️ canusetranslated:"
echo "  checkstatus: python scripts/monitor_whisper.py"
echo "  cleantranslated: python scripts/monitor_whisper.py --kill-duplicates"
echo "  translatedSystem: ./stop_autoclip.sh"
