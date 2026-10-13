# ignored at start
D=/usr/bin/dash
trap '' TERM USR1 HUP
$D -c 'trap "echo trapped" TERM; echo "set=$?"; trap; kill -TERM $$; echo not-trapped'
$D -c 'trap - TERM; echo "reset=$?"; kill -TERM $$; echo still-ignored'
$D -c 'trap "echo t" USR1; trap "echo i" INT; echo "listed: $(trap | tr "\n" ";")"; trap > o; cat o; kill -USR1 $$; echo usr1-ignored'
$D -c 'trap "" TERM; echo "ign=$?"; trap > o; cat o; echo "--"; trap - TERM; trap > o; cat o; echo end'
$D -c '(trap "echo sub" TERM; kill -TERM $$; echo sub-not-trapped)'
$D -c 'sleep 5 & p=$!; kill -TERM $p; wait $p; echo "child of child: $?"'
$D -c "$D -c 'trap \"echo gg\" HUP; kill -HUP \$\$; echo grandchild-ignored'"
echo "--- interactive child may trap"
$D -i -c 'trap "echo trapped-i" TERM; kill -TERM $$; echo after-i' 2>/dev/null
echo "--- exec keeps"
$D -c 'exec '$D' -c "trap \"echo t\" TERM; kill -TERM \$\$; echo exec-kept-ignored"'
trap - TERM USR1 HUP
echo "--- traps reset on exec / subshell"
trap 'echo parent-usr1' USR1
$D -c 'kill -USR1 $$; echo wrongly-alive'; echo "child default: $?"
(kill -USR1 $$; echo sub-after) ; echo "sub: $?"
( trap; echo "sub-traps-listed-above" )
(trap 'echo sub-own' USR1; kill -USR1 $$; echo sub-done); echo "st=$?"
echo "--- trap '' inherited by subshell and exec"
trap '' USR2
(kill -USR2 $$; echo sub-ignored)
$D -c 'kill -USR2 $$; echo child-ignored'
trap - USR2
echo "--- cmdsub"
x=$(trap 'echo cs' USR1; kill -USR1 $$; echo cs-done); echo "[$x]"
echo end
