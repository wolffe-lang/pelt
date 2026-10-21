#!/bin/bash
# sh23: every probe under every shell and mode, inside ctr.sh's container
# (dash, bash and zsh run as binaries from kasumi's /usr, never read).
# usage: run.sh OUTDIR PELT...   (each PELT a built binary: name=path)
# Each run: a scratch TMPDIR, HOME and XDG of its own, the probe on
# standard input (`-i`) or as a file; stdout, stderr and the exit status
# kept as OUTDIR/<shell>-<mode>/<probe>.{out,err,exit}.
set -u
P=$(cd "$(dirname "$0")" && pwd)
OUT=$1; shift
mkdir -p "$OUT"
one() { # label probe argv...
    local label=$1 probe=$2; shift 2
    local d="$OUT/$label" w; mkdir -p "$d"
    w=$(mktemp -d "${TMPDIR:-/tmp}/sh23-probe.XXXXXX")
    mkdir -p "$w/home" "$w/cfg" "$w/data" "$w/tmp" "$w/w"
    local base; base=$(basename "$probe"); base=${base%.*}
    (cd "$w/w" && env -i PATH=/usr/bin:/bin HOME="$w/home" XDG_CONFIG_HOME="$w/cfg" \
        XDG_DATA_HOME="$w/data" TMPDIR="$w/tmp" LC_ALL=C TERM=dumb "$@") \
        >"$d/$base.out" 2>"$d/$base.err"
    echo $? >"$d/$base.exit"
    chmod -R u+rwx "$w" 2>/dev/null; rm -rf "$w"
}
for p in ${PROBES:-"$P"/sh/p0*.sh "$P"/sh/p1*.sh}; do
    one dash-i "$p" sh -c 'exec dash -i <"$0"' "$p"
    one bash-i "$p" sh -c 'exec bash --norc --noprofile -i <"$0"' "$p"
    one bash-i-autocd "$p" sh -c 'exec bash --norc --noprofile -i -O autocd <"$0"' "$p"
    one bash-posix-i-autocd "$p" sh -c 'exec bash --posix --norc --noprofile -i -O autocd <"$0"' "$p"
    one zsh-i-autocd "$p" sh -c 'exec zsh -f -i -o autocd <"$0"' "$p"
    for spec in "$@"; do
        n=${spec%%=*}; b=${spec#*=}
        one "$n-i" "$p" sh -c 'exec "$1" -i <"$0"' "$p" "$b"
    done
done
for p in "$P"/sh/p2*.sh; do
    one dash-script "$p" dash "$p"
    one bash-script-autocd "$p" bash -O autocd "$p"
    one bash-c-autocd "$p" sh -c 'exec bash -O autocd -c "$(cat "$0")"' "$p"
    one bash-stdin-autocd "$p" sh -c 'exec bash -O autocd <"$0"' "$p"
    one zsh-script-autocd "$p" zsh -f -o autocd "$p"
    one zsh-c-autocd "$p" sh -c 'exec zsh -f -o autocd -c "$(cat "$0")"' "$p"
    one zsh-stdin-autocd "$p" sh -c 'exec zsh -f -o autocd <"$0"' "$p"
    for spec in "$@"; do
        n=${spec%%=*}; b=${spec#*=}
        one "$n-script" "$p" "$b" "$p"
    done
done
bash --version | head -1; zsh --version; pacman -Q dash bash zsh 2>/dev/null
echo "run.sh: done"
