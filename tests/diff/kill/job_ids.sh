# A job id names one of the shell's own asynchronous lists (XCU `kill`,
# XBD 3.182): by number, and the newest by %%. The oracle here is bash:
# dash 0.5.13.4 answers "no such process" for every `kill %n` in a
# script (it signals a process group the job does not have without
# `set -m`), where XCU `kill` says the job is signalled.
sleep 2 & sleep 3 &
kill -0 %1 %2; echo "both=$?"
kill %%; wait %2 2>/dev/null; echo "newest: $(kill -l $?)"
kill -s KILL %1; wait %1 2>/dev/null; echo "first: $(kill -l $?)"
sleep 2 &
kill %+; wait $! 2>/dev/null; echo "plus: $(kill -l $?)"
