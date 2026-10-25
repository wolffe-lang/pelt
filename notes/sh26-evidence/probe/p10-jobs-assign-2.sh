# item 6 (pelt#56): more job texts, and whether dash's substitution text repeats
set -m
>/dev/null & wait; jobs
p=1 2>&1 & wait; jobs
FOO=bar cmdx arg 2>/dev/null & wait; jobs
x=1 y=2 true >/dev/null & wait; jobs
FOO=$(echo a) & wait; jobs
FOO=$(echo a) & wait; jobs
FOO="$(echo a)" & wait; jobs
FOO=`echo a` & wait; jobs
FOO=$((1+2)) & wait; jobs
FOO=${HOME} & wait; jobs
true FOO=$(echo a) & wait; jobs
