# pelt#17, XCU set -x: an assignment-only command is traced too, its
# values expanded and unquoted, after what its substitutions traced; a
# command's redirections are not written, and the trace goes where
# standard error was before them
exec 2>&1
set -x
y=1
z='a b' w=$z
v=$(echo sub)
x=1 >/dev/null
y=2 true
echo hi >/dev/null 2>&1
set +x
