{ echo a; echo b >&2; echo c > f2; } > f1 2>&1; cat f1 f2
for i in 1 2; do echo $i; done > f3; cat f3
if true; then cat; fi < f3
( echo sub ) > f4; cat f4
case x in x) echo in-case;; esac > f5; cat f5
