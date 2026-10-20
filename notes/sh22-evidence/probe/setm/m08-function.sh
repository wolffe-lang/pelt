# set -m in a script: jobs started in a function called twice
set -m
f() { sh -c "exit $1" & sleep 0.3; echo "f $1 returns" >&2; }
f 1
echo "after f 1" >&2
f 2; echo "same line as f 2" >&2
echo "the next line" >&2
