exec 2>&-
exec /bin/sh -c 'echo to-err >&2; echo st=$?' 2>/dev/null
