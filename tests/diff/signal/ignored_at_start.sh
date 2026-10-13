# A signal that was ignored when a shell started cannot be trapped or
# reset (XCU `trap`): the trap is recorded and listed, and the signal
# still does nothing, in a subshell, after `exec` and in the shell's
# own children too. One that was not ignored is trapped as ever.
trap '' TERM USR1 HUP
../sh -c 'trap "echo trapped" TERM; echo "set=$?"; trap; kill -TERM $$; echo not-trapped'
../sh -c 'trap - TERM; echo "reset=$?"; kill -TERM $$; echo still-ignored'
../sh -c 'trap "echo t" USR1; trap "echo int-trapped" INT; trap; kill -USR1 $$; echo usr1-ignored; kill -INT $$; echo after-int'
../sh -c 'trap "" TERM; trap; echo --; trap - TERM; trap; echo end'
../sh -c '(trap "echo sub" TERM; kill -TERM $$; echo sub-not-trapped)'
../sh -c 'x=$(trap "echo cs" TERM; kill -TERM $$; echo cs-not-trapped); echo "$x"'
../sh -c '../sh -c "trap \"echo gg\" HUP; kill -HUP \$\$; echo grandchild-ignored"'
../sh -c 'exec ../sh -c "trap \"echo t\" TERM; kill -TERM \$\$; echo exec-kept-ignored"'
../sh -c 'sleep 1 & p=$!; kill -TERM $p; wait $p; echo "a child inherits it: $?"'
trap - TERM USR1 HUP
../sh -c 'trap "echo trapped-again" TERM; kill -TERM $$; echo after'
