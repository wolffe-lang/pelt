#!/bin/sh
# witness.sh — the sh07 access witness, black-box, in a container.
# usage: witness.sh PELT_STATIC IMAGE PODMAN...
# Runs access.sh under the image's dash and under a static pelt, as root
# and as uid 1000, with this directory mounted read-only at /s (so that
# `-w /s/access.sh` asks a read-only mount), each in a fresh directory
# under the container's /tmp; then dirsize.sh under dash on a tmpfs and
# on the container's own filesystem. Network off; nothing of the host
# but this directory and the pelt binary is mounted.
set -u
pelt=$1 image=$2
shift 2
here=$(cd "$(dirname "$0")" && pwd)
for who in 0:0 1000:1000; do
    for sh in /usr/bin/dash /p/pelt; do
        echo "== uid:gid $who, $sh"
        "$@" run --rm --network none --user "$who" \
            -v "$here:/s:ro" -v "$pelt:/p/pelt:ro" "$image" \
            /bin/sh -c "cd \"\$(mktemp -d)\" && $sh /s/access.sh; echo \"exit \$?\""
    done
done
echo "== dirsize, tmpfs"
"$@" run --rm --network none --tmpfs /t -v "$here:/s:ro" "$image" \
    /bin/sh -c 'cd /t && /usr/bin/dash /s/dirsize.sh; stat -c "%s bytes, %F" d'
echo "== dirsize, the container's filesystem"
"$@" run --rm --network none -v "$here:/s:ro" "$image" \
    /bin/sh -c 'cd "$(mktemp -d)" && /usr/bin/dash /s/dirsize.sh; stat -c "%s bytes, %F" d'
