# One open of a FIFO for a command that is not found (XCU 2.9.1): the
# reader sees one end of file, and the shell does not open the FIFO a
# second time to wait for a reader that has gone. A second reader comes
# only if the script is not finished with the FIFO after five seconds,
# so a second open shows in the output instead of hanging (pelt#156).
mkfifo p
(cat p >/dev/null; echo "first reader: end of file") &
first=$!
/bin/sh -c 'i=0; while [ ! -e finished ] && [ $i -lt 50 ]; do sleep 0.1; i=$((i+1)); done
[ -e finished ] || { cat p >/dev/null; echo "second reader was needed"; }' &
no_such_utility_for_this_case >p
st=$?
wait "$first"
: >finished
wait
echo "status $st"
