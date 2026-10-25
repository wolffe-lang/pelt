# pelt#17: -o notify and -o ignoreeof in $- (dash's letters b and I, in
# dash's order) and in set +o, so that eval "$(set +o)" puts them back
(set -o ignoreeof; echo "$-")
(set -o ignoreeof -a -C -u -f -e -b; echo "$-")
(set -uaCvxbfe -o ignoreeof 2>/dev/null; echo "$-" >&3) 3>&1 2>/dev/null
(set -bm; echo "$-")
set -o ignoreeof -o notify
set +o | grep -E 'ignoreeof|notify'
saved=$(set +o)
set +o ignoreeof +o notify
case $- in *b*|*I*) echo still-on;; *) echo off;; esac
eval "$saved"
case $- in *b*) case $- in *I*) echo restored;; esac;; esac
set +o ignoreeof
