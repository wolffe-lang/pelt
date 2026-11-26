# The same for an input redirection: the FIFO's writer is met by one
# open, and the shell does not open the FIFO again to wait for a writer
# that has gone. A second writer comes only if the script is not
# finished with the FIFO after five seconds (pelt#156).
mkfifo p
(: >p; echo "first writer: opened and closed") &
first=$!
/bin/sh -c 'i=0; while [ ! -e finished ] && [ $i -lt 50 ]; do sleep 0.1; i=$((i+1)); done
[ -e finished ] || { : >p; echo "second writer was needed"; }' &
no_such_utility_for_this_case <p
st=$?
wait "$first"
: >finished
wait
echo "status $st"
