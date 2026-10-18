#!/bin/bash
# sh18: the references measured, black-box, inside refrun.sh's container.
# usage (inside the container): run.sh OUTDIR [keys-or-script ...]
P=$(cd "$(dirname "$0")" && pwd)
export PELT_TREE=${PELT_TREE:-$P/../../..}
O=$1; shift
mkdir -p "$O"
items=("$@")
[ ${#items[@]} -eq 0 ] && items=($P/keys/*.keys $P/scripts/*.sh)
for f in "${items[@]}"; do
  b=$(basename "$f"); b=${b%.*}
  case $f in
  *.keys)
    for sh in dash bash; do
      if [ $sh = dash ]; then a=(dash -i -m); else a=(bash --posix -i -m); fi
      python3 "$P/jcprobe.py" "$f" "${a[@]}" > "$O/$b.$sh.txt" 2>&1
    done ;;
  *.sh)
    for sh in dash bash; do
      if [ $sh = dash ]; then a=(dash); else a=(bash --posix); fi
      d=$(mktemp -d "$TMPDIR/sh18p.XXXXXX")
      ( cd "$d" && setsid -w timeout 20 "${a[@]}" "$f" < /dev/null > "$d/out" 2> "$d/err"; echo "exit=$?" > "$d/st" )
      { echo "\$ ${a[*]} $b"; echo "--out"; cat "$d/out"; echo "--err"; cat "$d/err"; cat "$d/st"; } > "$O/$b.$sh.txt"
      rm -rf "$d"
    done ;;
  esac
  echo "done $b"
done
