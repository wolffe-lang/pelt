# `.` reads any file that is not a directory: /dev/null is an empty
# script, and a FIFO is read until its writer closes it (XCU 2.15 dot).
# The writer here is a program, so the shell need not run two things
# at once; builtin/c_s_dot_special_file has the shell itself write it.
. /dev/null
echo "dev null: $?"
mkfifo pipe
/usr/bin/env sh -c 'echo "echo from the fifo; v=set" >pipe' &
. ./pipe
echo "fifo: $? v=$v"
wait
