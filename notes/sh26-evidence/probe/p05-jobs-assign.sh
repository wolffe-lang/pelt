# item 6 (pelt#56): the job text of assignment-only commands
set -m
FOO=bar & wait; jobs
FOO=bar BAZ=q & wait; jobs
FOO=bar true & wait; jobs
( p=1; echo x >/dev/null; : ) & wait; jobs
{ p=1; : ; } & wait; jobs
p=1 >/dev/null & wait; jobs
FOO=$(echo a) & wait; jobs
