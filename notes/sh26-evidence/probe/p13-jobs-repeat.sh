# item 6: dash's job text for assignment-only commands, run after run
set -m
FOO=bar & wait; jobs
FOO=bar BAZ=q & wait; jobs
FOO=$(echo a) & wait; jobs
