set -e
case $- in *e*) echo has-e;; esac
set +e
case $- in *e*) echo still;; *) echo no-e;; esac
