#!/usr/bin/env bash
# Host-side negative/positive control; only --user differs between containers.
set -eu
root=/home/mfwolffe/lanes/sh35
slot=$1
[ "$(git -C "$root/main-f423b34" rev-parse HEAD)" = f423b342041b9debba3e5222ad4347a19b18979f ]
[ -z "$(git -C "$root/main-f423b34" status --porcelain --untracked-files=no)" ]
mkdir -p "$root/permission-home" "$root/permission-tmp"
for uid in 0 1000; do
    log="$root/permission-uid-$uid.log"
    set +e
    podman run --rm --memory 12g --userns keep-id --user "$uid:$uid" \
      -v "$root:/lane" -v "$root/main-f423b34:/work" -w /work \
      -e HOME=/lane/permission-home -e TMPDIR=/lane/permission-tmp \
      localhost/r41-toolchain:1 /usr/bin/taskset.real -c "$slot" bash -c '
        set -eu
        echo "UID_CONTROL uid=$(id -u) gid=$(id -g)"
        grep -E "^(CapEff|Cpus_allowed_list):" /proc/self/status
        sha256sum target/native/pelt
        set +e
        tools/difftest --bin target/native glob/c_unreadable test/c_permissions test/c_s_test_access
        code=$?
        echo "END permission-uid-$(id -u) exit=$code"
        exit "$code"
      ' < /dev/null > "$log" 2>&1
    code=$?
    set -e
    cat "$log"
    grep -q "^UID_CONTROL uid=$uid gid=$uid$" "$log"
    if [ "$uid" = 0 ]; then
        [ "$code" = 1 ]
        grep -Eq '^difftest: total +0 +3 +0 ' "$log"
        for row in glob/c_unreadable test/c_permissions test/c_s_test_access; do
            grep -q "^FAIL $row: stdout$" "$log"
        done
    else
        [ "$code" = 0 ]
        grep -Eq '^difftest: total +3 +0 +0 ' "$log"
        for row in glob/c_unreadable test/c_permissions test/c_s_test_access; do
            grep -q "^ok   $row$" "$log"
        done
    fi
done
[ -z "$(git -C "$root/main-f423b34" status --porcelain --untracked-files=no)" ]
echo 'END permission-comparison exit=0'
