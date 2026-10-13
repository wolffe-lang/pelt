# `$?` after a child a signal ended is 128 plus the signal's number,
# and `kill -l $?` names it (XCU 2.8.2, `kill`).
for s in HUP INT USR1 USR2 PIPE ALRM TERM VTALRM PROF KILL; do
  ../sh -c "kill -s $s \$\$; echo survived"
  st=$?
  [ $st -gt 128 ] && echo "$s -> $(kill -l $st)"
done
for s in CONT WINCH URG CHLD; do
  ../sh -c "kill -s $s \$\$; echo survived-$s"; echo "$s -> $?"
done
