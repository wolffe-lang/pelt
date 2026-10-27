set -m -o nolog
saved=$(set +o)
printf '%s\n' "$saved" | grep -E ' (monitor|nolog)$'
set +m +o nolog
eval "$saved"
case $- in *m*) echo monitor-restored;; *) echo monitor-lost;; esac
set -o | grep -E '^(monitor|nolog)[[:space:]]' | awk '{print $1, $2}'
(set +o nolog; set -o | grep '^nolog' | awk '{print $1, $2}')
set -o | grep '^nolog' | awk '{print $1, $2}'
