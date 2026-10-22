#!/bin/bash
# sh24: frozen baseline/head copies, dash; three interleaved passes.
set -u
S=$(cd "$(dirname "$0")" && pwd)
cd "$S/head" || exit 9
ulimit -c 0
only=baseline,jobs-loop,jobs-set-m,compound-brace-redir,compound-if-redir,compound-while-redir
for pass in 1 2 3; do
  for mode in bare four; do
    for bin in "$S/base/target/native/pelt" "$S/head/target/native/pelt" "$S/base/target/release/pelt" "$S/head/target/release/pelt" /usr/bin/dash; do
      tag=$(echo "$bin" | sed "s,$S/,,; s,/target/,_,g; s,/pelt,,; s,/usr/bin/,,")
      out="$S/logs/table-$pass-$mode-$tag.log"
      echo "pass=$pass mode=$mode binary=$bin $(uptime)" | tee "$out"
      if [ "$mode" = four ]; then
        taskset -c 8-11 tools/shape-rss --only "$only" "$bin" >> "$out" 2>&1
      else
        tools/shape-rss --only "$only" "$bin" >> "$out" 2>&1
      fi
      echo "exit=$?" >> "$out"
      tail -1 "$out"
    done
  done
done
# The 10,000-call check uses anonymous memory, not mapped pages.
for mode in bare four; do
  echo "jobs anonymous mode=$mode $(uptime)"
  if [ "$mode" = four ]; then cmd=(taskset -c 8-11); else cmd=(); fi
  "${cmd[@]}" python3 "$S/probe/jobs-anon.py" "$S/base/target/native/pelt" "$S/head/target/native/pelt" "$S/base/target/release/pelt" "$S/head/target/release/pelt" /usr/bin/dash > "$S/logs/jobs-anon-$mode.log" 2>&1
done
