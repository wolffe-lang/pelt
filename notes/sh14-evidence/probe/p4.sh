# $$ and $PPID
echo "pid-num: $(case $$ in *[!0-9]*|'') echo bad;; *) echo ok;; esac)"
a=$$; ( [ "$a" = "$$" ] && echo sub-same ); [ "$a" = "$(echo $$)" ] && echo cs-same
echo x | { read l; [ "$a" = "$$" ] && echo pipe-same; }
( [ "$a" = "$$" ] && echo bg-same ) & wait
[ "$(/usr/bin/dash -c 'echo $PPID')" = "$$" ] && echo child-ppid-is-me
p=$PPID; ( [ "$p" = "$PPID" ] && echo ppid-sub-same )
PPID=7 2>/dev/null; echo "assign st=$? PPID=$( [ "$PPID" = 7 ] && echo changed || echo kept)"
(unset PPID 2>/dev/null; echo "unset st=$? [${PPID:+set}]")
(readonly -p | grep -c PPID)
(export -p | grep -c PPID)
env | grep -c '^PPID='
(set | grep -c '^PPID=')
PPID=5 /usr/bin/dash -c 'echo "env PPID honoured: $( [ "$PPID" = 5 ] && echo yes || echo no)"'
'$'=3 2>/dev/null; echo "st=$?"
echo "${$:+dollar-set}" "${#$}" | sed 's/[0-9][0-9]*/N/'
echo "--- status after signals"
/usr/bin/dash -c 'kill -TERM $$'; s=$?; echo "$s $(kill -l $s)"
/usr/bin/dash -c 'kill -KILL $$'; s=$?; echo "$s $(kill -l $s)"
/usr/bin/dash -c 'kill -USR1 $$'; s=$?; echo "$s $(kill -l $s)"
/usr/bin/dash -c 'kill -PIPE $$'; s=$?; echo "$s $(kill -l $s)"
sleep 5 & kill -USR2 $!; wait $!; s=$?; echo "$s $(kill -l $s)"
