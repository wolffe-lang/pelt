# `trap` with no operands lists EXIT first and then the signals in the
# order of their numbers, whatever order they were set in (dash; POSIX
# asks only that the output can be read back). Signals whose order is
# the same on every host.
trap 'a' TERM; trap 'b' HUP; trap 'd' EXIT; trap 'e' WINCH
trap '' INT; trap 'f' 14; trap 'g' ABRT; trap 'h' PIPE; trap 'i' QUIT
trap
trap - TERM HUP EXIT WINCH INT ALRM ABRT PIPE QUIT
trap
echo "left=$?"
