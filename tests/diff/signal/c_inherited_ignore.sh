trap '' TERM
../sh -c 'kill -TERM $(sh -c "echo \$PPID"); echo child-ignores'
trap - TERM
../sh -c 'trap "echo child-traps" TERM; kill -TERM $(sh -c "echo \$PPID"); echo after'
