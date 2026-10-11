set -f; case $- in *f*) echo f-on;; esac
set +f; case $- in *f*) echo f-still;; *) echo f-off;; esac
set -eu; case $- in *e*) case $- in *u*) echo eu;; esac;; esac
