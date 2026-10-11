export a='x y' b="it's" c; d=notexported
export -p | grep -E ' (a|b|c|d)(=|$)' | sort
saved=$(export -p | grep -E ' (a|b)='); unset a b; eval "$saved"; sh -c 'echo "$a $b"'
