set -o noglob; case $- in *f*) echo f;; esac; set +o noglob
set -o errexit -o nounset; case $- in *e*) case $- in *u*) echo eu;; esac;; esac; set +o errexit +o nounset
set -o allexport; case $- in *a*) echo a;; esac; set +o allexport
set -o noclobber; case $- in *C*) echo C;; esac; set +o noclobber
set -o verbose 2>/dev/null; case $- in *v*) echo v;; esac; set +o verbose 2>/dev/null
set -o xtrace 2>/dev/null; case $- in *x*) set +o xtrace 2>/dev/null; echo x;; esac
set -o notify; case $- in *b*) echo b;; esac; set +o notify
