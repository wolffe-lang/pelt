# run by hand: the interactive ignoreeof and MAIL probes (pty.py)
P=/home/mfwolffe/lanes/sh26/probe
for sh in /usr/bin/dash /usr/bin/bash "$PELT"; do
  echo "##### $sh ignoreeof"
  python3 -I $P/pty.py 0.5 'PS1=$\s' $sh -i +m -- 'set -o ignoreeof' '^D' 'echo still-here' '^D' '^D' 'set +o ignoreeof' 'echo $-' 'exit'
  echo "##### $sh ignoreeof x12"
  python3 -I $P/pty.py 0.3 'PS1=$\s' $sh -i +m -- 'set -o ignoreeof' '^D' '^D' '^D' '^D' '^D' '^D' '^D' '^D' '^D' '^D' '^D' '^D' 'echo alive'
done
