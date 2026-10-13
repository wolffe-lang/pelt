# `kill` is built in: it works with no PATH to search, and inside a
# function and a subshell.
PATH=/nonexistent
kill -0 $$; echo "no-path=$?"
f() { kill -0 $$; }; f; echo "function=$?"
( kill -0 $$ ); echo "subshell=$?"
x=$(kill -l 15); echo "cmdsub=$x"
kill -l 9 | { read n; echo "pipe=$n"; }
