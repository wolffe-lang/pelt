# `trap '' CHLD` does not cost the shell its children's statuses: a
# foreground program, a waited job, a command substitution and a
# pipeline all still answer.
trap '' CHLD
/bin/sh -c 'exit 3'; echo "st=$?"
sleep 0.1 & wait $!; echo "bg=$?"
x=$(/bin/sh -c 'echo out; exit 4'); echo "cs=$? $x"
/bin/sh -c 'exit 5' | /bin/sh -c 'exit 6'; echo "pipe=$?"
trap
trap - CHLD
/bin/sh -c 'exit 7'; echo "st=$?"
