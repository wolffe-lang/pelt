echo a >> f; echo b >> f; echo c 1>>f; cat f
exec 3>>f; echo d >&3; echo e >> f; echo f2 >&3; exec 3>&-; cat f
