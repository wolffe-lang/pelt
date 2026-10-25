# run by hand: MAILCHECK timing and what counts as new mail (pty.py)
P=/home/mfwolffe/lanes/sh26/probe
H=$HOME/mailh
for sh in /usr/bin/dash /usr/bin/bash "$PELT"; do
  rm -rf $H; mkdir -p $H
  echo "##### $sh env MAIL, MAILCHECK=100"
  PROBE_HOME=$H python3 -I $P/pty.py 0.4 "MAIL=$H/mbox MAILCHECK=100" $sh -i +m -- 'echo a > $HOME/mbox' 'echo b >> $HOME/mbox' ':' 'echo c >> $HOME/mbox' 'exit'
  rm -rf $H; mkdir -p $H; echo pre > $H/mbox
  echo "##### $sh env MAIL existing, MAILCHECK=0, same-size rewrite, touch"
  PROBE_HOME=$H python3 -I $P/pty.py 0.4 "MAIL=$H/mbox MAILCHECK=0" $sh -i +m -- ':' 'echo b > $HOME/mbox' '@1.1' 'echo c > $HOME/mbox' 'touch $HOME/mbox' 'echo dd > $HOME/mbox' 'rm $HOME/mbox' 'echo e > $HOME/mbox' 'exit'
  rm -rf $H; mkdir -p $H
  echo "##### $sh MAILPATH quoted messages"
  PROBE_HOME=$H python3 -I $P/pty.py 0.4 "MAILCHECK=0" $sh -i +m -- 'MAILPATH='"'"'$HOME/m2%got $HOME:$HOME/m3%three:$HOME/a\%b'"'" 'echo z > $HOME/m2' 'echo w > $HOME/m3' 'echo v > $HOME/a%b' 'exit'
done
