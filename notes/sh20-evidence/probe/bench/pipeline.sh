# bench/pipeline.sh — 1,000 three-stage pipelines: a built-in feeding
# two programs.
i=0
while [ "$i" -lt 1000 ]; do
    echo x | cat | cat >/dev/null
    i=$((i + 1))
done
