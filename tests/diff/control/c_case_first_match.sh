x=abc
case $x in a*) echo first;; abc) echo second;; esac
case $x in z) echo no;; $(echo evaluated >&2; echo q)) echo no;; a?c) echo third;; $(echo never >&2)) ;; esac 2>&1
