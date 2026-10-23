#!/bin/bash
# Other lanes' affinity does not measure this lane's assigned cores.
set -eu
while true; do
    uptime
    if python3 -I - <<'PY'
import time

def cpus():
    out = {}
    with open('/proc/stat') as f:
        for line in f:
            k, *v = line.split()
            if k in ('cpu12', 'cpu13', 'cpu14', 'cpu15'):
                v = list(map(int, v[:8]))
                out[k] = (sum(v), v[3] + v[4])
    return out

a = cpus()
time.sleep(5)
b = cpus()
assert len(a) == len(b) == 4
idle = {k: 100 * (b[k][1] - a[k][1]) / (b[k][0] - a[k][0]) for k in a}
print('assigned-core idle percent over5s:', idle, flush=True)
raise SystemExit(0 if min(idle.values()) >= 90 else 1)
PY
    then break; fi
    sleep 60
done
exec "$@"
