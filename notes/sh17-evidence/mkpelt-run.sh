#!/bin/bash
# sh17: pax's tools/mkpelt at pax trunk, inside Ubuntu 24.04, against pelt REV
set -euo pipefail
REV=$1
cd /work
git clone -q https://github.com/wolffe-lang/pax.git pax
cd pax
echo "pax $(git rev-parse HEAD)"
sed -i "s/^PELT_REV=.*/PELT_REV=$REV/" user/pelt.pin
grep ^PELT_REV user/pelt.pin
TMPDIR=/work/tmp PAX_CACHE=/work/cache tools/mkpelt /out
readelf -hW /out/pelt | grep Type
readelf -lW /out/pelt | grep -c INTERP || true
sha256sum /out/pelt
