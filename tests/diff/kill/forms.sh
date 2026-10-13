# Every way XCU `kill` names a signal: -s name, -s number, -name,
# -number, in any case, and `--` before the operands. The child's
# status says which signal came.
for how in '' '-s TERM' '-s term' '-s Term' '-TERM' '-term' '-s 15' '-15' '-s KILL' '-KILL' '-9' '-s HUP' '-hup' '-1' '-s USR1' '-USR1' '-s USR2' '-s ALRM' '-s PIPE' '-s VTALRM' '-s PROF' '--' '-s TERM --' '-s HUP -s KILL' '-sKILL'; do
  sleep 5 & p=$!
  kill $how $p; k=$?
  wait $p
  echo "[$how] kill=$k $(kill -l $?)"
done 2>/dev/null
