set -- 'a b' c
unset u
for i in ${u:-"$@"}; do echo "[$i]"; done
for i in "${u:-$@}"; do echo "[$i]"; done
