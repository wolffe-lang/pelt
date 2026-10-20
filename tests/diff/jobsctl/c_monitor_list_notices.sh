# set -m in a script: a job is told after the complete command it ended
# in: after the whole line, after a brace group (not inside it), after
# the command that called a function (dash, black-box:
# notes/sh22-evidence/refs/setm-base/m03, m08; pelt#41)
exec 2>&1
set -m
sh -c 'exit 4' & wait $!
echo "after the first job's line"
{ sh -c 'exit 5' & wait $!; echo "inside the group"; }
echo "after the group"
f() { sh -c "exit $1" & wait $!; echo "f $1 returns"; }
f 6
echo "after f 6"
f 7; echo "same line as f 7"
echo "the next line"
