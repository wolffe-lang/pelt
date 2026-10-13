# CHLD can be trapped: the action runs when a child ends.
trap 'echo child-ended' CHLD
/bin/sh -c 'exit 3'; echo "st=$?"
trap - CHLD
/bin/sh -c 'exit 4'; echo "st=$?"
