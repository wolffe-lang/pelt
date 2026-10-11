set -- 'a b' c ''
for i in "$@"; do echo "[$i]"; done
for i in "x$@y"; do echo "[$i]"; done
