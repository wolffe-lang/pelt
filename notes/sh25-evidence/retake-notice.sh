#!/bin/bash
# Compare unchanged rows with the same shell, not dash's diagnostic wording.
set -u
S=/home/mfwolffe/lanes/sh25
cd "$S/pelt" || exit 9
ulimit -c 0
ST=$S/logs/notice-retake.status
: > "$ST"
for tier in native release; do
 echo "$(date -Is) $tier $(uptime)" | tee -a "$ST"
 bash notes/sh25-evidence/notice5-before.sh "$S/base-bin/$tier/pelt" > "$S/logs/notice-before-$tier.log" 2>&1
 echo "notice-before-$tier=$?" | tee -a "$ST"
 bash notes/sh20-evidence/probe/notice5.sh "$S/pelt/target/$tier/pelt" > "$S/logs/notice-retake-$tier.log" 2>&1
 echo "notice-$tier=$?" | tee -a "$ST"
 python3 -I notes/sh25-evidence/check-notice5.py "$S/logs/notice-before-$tier.log" "$S/logs/notice-retake-$tier.log" > "$S/logs/notice-retake-check-$tier.log" 2>&1
 echo "notice-check-$tier=$?" | tee -a "$ST"
done
echo done | tee -a "$ST"
