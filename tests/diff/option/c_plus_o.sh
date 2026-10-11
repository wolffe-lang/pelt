set -f -u
saved=$(set +o)
set +f +u
eval "$saved"
case $- in *f*) case $- in *u*) echo restored;; esac;; esac
set -o | grep -c . | sed 's/[0-9][0-9]*/some-lines/'
set +o | grep -E 'noglob|nounset|errexit' | sort
