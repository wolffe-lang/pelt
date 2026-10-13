# A trap for a signal nothing can catch (KILL, STOP) is not an error
# and is listed (dash). pelt records the fault signals the same way.
trap ':' KILL STOP; echo "st=$?"
trap | sort
trap - KILL STOP
trap ':' SEGV BUS FPE ILL TRAP SYS; echo "st=$?"
trap | sort
trap - SEGV BUS FPE ILL TRAP SYS; trap; echo "st=$?"
