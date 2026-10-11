HOME=$PWD
echo hi > ~/f; cat f
case $PWD in ~) echo matched;; esac
case ~ in "$PWD") echo matched2;; esac
