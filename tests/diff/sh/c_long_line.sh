x=$(printf '%05000d' 0)
y=$(printf 'echo %s' "$x$x$x$x$x$x$x$x")
../sh -c "$y" | wc -c | tr -d ' '
