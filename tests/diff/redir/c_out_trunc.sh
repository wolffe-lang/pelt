echo long-content > f; echo s > f; cat f
: > f; wc -c < f | tr -d ' '
echo e 2>g 1>&2; cat g
