# Control for the once_ rows (pelt#156): a command that is found opens
# a FIFO once; its reader sees one end of file and no second reader is
# needed (the same bounded wait as once_notfound_fifo_write).
mkfifo p
(cat p >/dev/null; echo "first reader: end of file") &
first=$!
/bin/sh -c 'i=0; while [ ! -e finished ] && [ $i -lt 50 ]; do sleep 0.1; i=$((i+1)); done
[ -e finished ] || { cat p >/dev/null; echo "second reader was needed"; }' &
true >p
st=$?
wait "$first"
: >finished
wait
echo "status $st"
