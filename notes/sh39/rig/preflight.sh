#!/usr/bin/env bash
# Run this alone before queueing, and again through the recorder under locks.
set -eu
: "${PELT_ENGINE:?set the approved container engine}"
root=$(git rev-parse --show-toplevel)
[ -z "$(git status --porcelain)" ] || { printf 'REFUSED checkout-dirty\n'; exit 75; }
if ps -C wineserver -o pid= | grep -q '[0-9]'; then printf 'REFUSED interactive-use\n'; exit 75; fi
python3 -I -c 'import shutil,sys; n=shutil.disk_usage(sys.argv[1]).free; print("free_bytes="+str(n)); sys.exit(0 if n>35*1024**3 else 75)' "$root"
for image in localhost/r41-toolchain:1 localhost/sh38-oracle:1; do
  "$PELT_ENGINE" image inspect --format '{{.Id}}' "$image"
  "$PELT_ENGINE" run --rm --entrypoint sh "$image" -c 'command -v python3; command -v cc; command -v dash; command -v bash; command -v taskset'
done
[ -x "$root/.wolf-bin/wolf" ] && [ -x "$root/.wolf-bin/lupin" ]
mkdir -p "$(dirname "$root")/container-temp"
bash notes/sh39/rig/container.sh localhost/r41-toolchain:1 sh -c '[ "$(id -u)" -ne 0 ] && test -w "$PELT_NOEXEC_DIR"'
bash notes/sh39/rig/container.sh localhost/sh38-oracle:1 python3 -c 'import unicodedata; assert unicodedata.unidata_version == "16.0.0"'
printf 'preflight ready\n'
