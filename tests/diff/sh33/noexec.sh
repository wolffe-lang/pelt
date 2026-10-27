echo before
set -n; echo not-run; printf bad > marker
set +n
echo not-run-either
