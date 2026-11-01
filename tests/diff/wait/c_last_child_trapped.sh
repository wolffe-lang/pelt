# The same with a trap set, so `wait` parks on the trapped signals and the
# child's end together (sh.jobs `jc_wait`), and still returns only once
# the last child has ended
trap 'echo usr1' USR1
(sleep 0.4; echo late > g) &
wait; echo "st=$?"; cat g
