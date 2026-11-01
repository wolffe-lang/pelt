# `wait` with no operand returns once every child has ended (XCU `wait`):
# the one child here writes its file after a pause, and the file is there
# when `wait` returns (sh34: c_all's two children end together, so a wait
# that returned with one still running could pass it)
(sleep 0.4; echo late > f) &
wait; echo "st=$?"; cat f
