#!/bin/sh
# loopmem — lane-local: peak RSS of pelt over loops whose body is one construct
P=$1
cd "$HOME/lanes/sh06/tmp" || exit 1
for body in 'true && true' '/bin/true' 'x=$(true)' 'true | true' '{ true; }' 'echo x | cat >/dev/null' 'case a in a) :;; esac' 'f' 'i=$i'; do
  for n in 5000 20000; do
    {
      echo 'f() { :; }'
      echo 'i=0'
      echo "while [ \$i -lt $n ]; do $body; i=\$((i+1)); done"
      echo 'echo $i'
    } > l.sh
    r=$(/usr/bin/time -f '%M' "$P" l.sh 2>&1 | tr '\n' ' ')
    echo "loop $n [$body]: out+KB $r"
  done
done
rm -f l.sh
