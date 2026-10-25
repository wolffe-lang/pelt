# pelt#56 (R-sh20-1: copy dash): a job's text leaves a simple command's
# assignments out, so an assignment-only command is no text at all, and
# every redirection has a blank before it
set -m
FOO=bar & wait; jobs
FOO=bar BAZ=q & wait; jobs
FOO=bar true & wait; jobs
( p=1; echo x >/dev/null; : ) & wait; jobs
{ p=1; : ; } & wait; jobs
p=1 >/dev/null & wait; jobs
>/dev/null & wait; jobs
x=1 y=2 true 2>/dev/null & wait; jobs
