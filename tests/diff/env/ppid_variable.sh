# PPID is set by the shell when it starts (XCU 2.5.3), whatever the
# environment said; after that it is an ordinary variable: the same in
# a subshell, not exported, assignable.
p=$PPID
( [ "$p" = "$PPID" ] && echo sub-same )
[ "$(echo $PPID)" = "$p" ] && echo cs-same
export -p | grep -c PPID
PPID=5 ../sh -c '[ "$PPID" = 5 ] && echo from-env || echo own'
[ "$(PPID=5 ../sh -c 'echo $PPID')" = "$$" ] && echo is-parent
PPID=7; echo "assigned=$PPID"
unset PPID; echo "unset=[${PPID-none}]"
