# set -m in a script, jobs started by separate commands, and inside a
# brace group: after which command is each reported?
set -m
sh -c 'exit 4' &
sleep 0.3
echo "after the first job's command" >&2
{ sh -c 'exit 5' & sleep 0.3; echo "inside the group" >&2; }
echo "after the group" >&2
sh -c 'exit 6' & sleep 0.3; echo "same line, after sleep" >&2
echo "the next line" >&2
