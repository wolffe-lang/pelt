case $PPID in *[!0-9]*|'') echo bad;; *) echo numeric;; esac
a=$PPID; (echo $PPID) | { read b; [ "$a" = "$b" ] && echo same; }
[ "$(sh -c 'echo $PPID')" != "$PPID" ] && echo child-differs
