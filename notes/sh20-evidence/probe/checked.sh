# sh20: the five shapes under the checked machine (ruling #95 R4 C):
# `os_fork` answers `unsupported` there and pelt runs each in process.
( echo sub-a; echo sub-b )
x=$(echo cs-a; echo cs-b); echo "cmdsub: $x"
{ echo brace-bg; } & wait
( echo paren-bg ) & wait
{ echo one; echo two; } | cat
f() { echo f-out; }; f | sed 's/^/stage: /'
( sleep 0.3; echo a ) & echo b; wait
( sleep 1 ) & p=$!; kill -0 $p 2>/dev/null && echo "bg-pid: a process" || echo "bg-pid: none"; wait
( echo redir-sub ) >/dev/null; { ( echo redir-brace ); } 2>/dev/null; echo "redir: $?"
echo "end $?"
