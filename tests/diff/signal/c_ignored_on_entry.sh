trap '' TERM
../sh -c 'trap "echo trapped" TERM; kill -TERM $$; echo not-trapped'
../sh -c 'trap - TERM; kill -TERM $$; echo still-ignored'
