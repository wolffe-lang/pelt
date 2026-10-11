trap 'echo a' INT TERM; trap - INT; trap | sed 's/SIG//'
trap 2 15; trap | wc -l | tr -d ' '
trap 'echo e' EXIT; trap 0; echo no-exit-trap
