#!/bin/bash
# sh21: every probe under every shell and mode, inside refrun.sh's
# container (dash, bash and fish run as binaries from kasumi's /usr, never
# read). usage: run.sh OUTDIR PELT...   (each PELT a built binary: name=path)
# Each run: a scratch TMPDIR, HOME and XDG of its own; stdout, stderr and
# the exit status kept as OUTDIR/<shell>-<mode>/<probe>.{out,err,exit}.
set -u
P=$(cd "$(dirname "$0")" && pwd)
OUT=$1; shift
mkdir -p "$OUT"
one() { # label probe argv...
    local label=$1 probe=$2; shift 2
    local d="$OUT/$label" w; mkdir -p "$d"
    w=$(mktemp -d "${TMPDIR:-/tmp}/sh21-probe.XXXXXX")
    mkdir -p "$w/home" "$w/cfg" "$w/data" "$w/tmp"
    local base; base=$(basename "$probe"); base=${base%.*}
    (cd "$w" && env -i PATH=/usr/bin:/bin HOME="$w/home" XDG_CONFIG_HOME="$w/cfg" \
        XDG_DATA_HOME="$w/data" TMPDIR="$w/tmp" LC_ALL=C TERM=dumb "$@") \
        >"$d/$base.out" 2>"$d/$base.err"
    echo $? >"$d/$base.exit"
    rm -rf "$w"
}
for p in "$P"/sh/*.sh; do
    one dash-script "$p" dash "$p"
    one dash-i "$p" sh -c 'exec dash -i <"$0"' "$p"
    one bash-posix-script "$p" bash --posix "$p"
    one bash-script "$p" bash "$p"
    one bash-i "$p" sh -c 'exec bash --norc --noprofile -i <"$0"' "$p"
    for spec in "$@"; do
        n=${spec%%=*}; b=${spec#*=}
        one "$n-script" "$p" "$b" "$p"
        one "$n-i" "$p" sh -c 'exec "$1" -i <"$0"' "$p" "$b"
    done
done
for p in "$P"/fish/*.fish; do
    one fish-script "$p" fish --no-config "$p"
    one fish-i "$p" sh -c 'exec fish --no-config -i <"$0"' "$p"
done
fish --version; bash --version | head -1; pacman -Q dash bash fish 2>/dev/null
echo "run.sh: done"
