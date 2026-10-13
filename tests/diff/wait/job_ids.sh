# `wait` takes a job id (XCU `wait`): the status of that asynchronous
# list; an id no job has is an error.
/bin/sh -c 'exit 3' &
/bin/sh -c 'exit 4' &
wait %1; echo "first=$?"
wait %2; echo "second=$?"
/bin/sh -c 'exit 5' &
wait %%; echo "newest=$?"
/bin/sh -c 'exit 6' &
wait %+; echo "plus=$?"
wait %9 2>/dev/null; echo "missing=$?"
