echo before
for x in one two; do echo "$x"; set -n; echo not-run; done
echo not-run-either
