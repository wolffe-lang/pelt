readonly a='x y' b
readonly -p | grep -E ' (a|b)(=|$)' | sort
