# item 5: the order of the letters in $- (notify's b, ignoreeof's I)
(set -o ignoreeof; echo "$-")
(set -o ignoreeof -a -C -u -f -e -b; echo "$-")
(set -o ignoreeof -m 2>/dev/null; echo "$-")
(set -uaCvxbfem -o ignoreeof -o noclobber 2>/dev/null; echo "$-" >&3) 3>&1 2>/dev/null
(set -bm; echo "$-")
(set -bx; echo "$-" >&3) 3>&1 2>/dev/null
(set -bv; echo "$-" >&3) 3>&1 2>/dev/null
(set -nb; echo "$-") ; echo n-done
