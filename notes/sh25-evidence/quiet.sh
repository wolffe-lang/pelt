#!/bin/bash
# Require two quiet minutes before starting a long measurement.
set -eu
quiet=0
while [ "$quiet" -lt 3 ]; do
    uptime
    if awk '{exit !($1 < 2)}' /proc/loadavg; then quiet=$((quiet+1)); else quiet=0; fi
    [ "$quiet" -ge 3 ] || sleep 60
done
exec "$@"
