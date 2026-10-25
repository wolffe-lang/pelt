# run by hand: job text for assignments, typed at dash -i -m (pty.py)
P=/home/mfwolffe/lanes/sh26/probe
for sh in /usr/bin/dash "$PELT"; do
  echo "##### $sh"
  python3 -I $P/pty.py 0.4 '' $sh -i -m -- 'a=1 sleep 0.3 &' '@0.6' 'jobs' 'FOO=bar &' '@0.3' 'jobs' 'p=1 >/dev/null &' '@0.3' 'jobs' 'FOO=$(echo a) &' '@0.3' 'jobs' 'exit'
done
