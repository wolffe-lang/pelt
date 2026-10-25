# pelt#17, XCU trap -p (new in POSIX.1-2024; dash 0.5.13.4 has none):
# each named condition's action as a command that sets it again, a
# default one as -, an ignored one as ''; an unknown name is status 1.
# Written to a file, not a pipe: a pipeline stage is a subshell, whose
# caught traps are back at the default (dash, as pelt; bash shows the
# shell's: sh26 probe/p28)
trap 'echo i' INT
trap '' QUIT
trap -p INT QUIT HUP > o; sed 's/SIG//' o
trap -p EXIT
trap -p NOSUCH 2>/dev/null; echo "st=$?"
trap -p > o; grep -E ' (INT|QUIT|HUP|EXIT)$' o | sed 's/SIG//'
eval "$(trap -p INT)"; trap > o; grep INT o
