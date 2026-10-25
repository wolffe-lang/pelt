# run by hand: the interactive MAIL, MAILPATH, MAILCHECK probes (pty.py)
P=/home/mfwolffe/lanes/sh26/probe
H=$HOME/mailh; 
for sh in /usr/bin/dash /usr/bin/bash "$PELT"; do
  rm -rf $H; mkdir -p $H; echo old > $H/pre
  echo "##### $sh MAIL MAILCHECK=0"
  PROBE_HOME=$H python3 -I $P/pty.py 0.5 '' $sh -i +m -- 'MAIL=$HOME/mbox MAILCHECK=0' 'echo x > $HOME/mbox' 'echo next' 'echo y >> $HOME/mbox' ': > $HOME/mbox' 'echo z > $HOME/mbox' 'MAIL=$HOME/pre' 'echo more >> $HOME/pre' 'exit'
  rm -rf $H; mkdir -p $H
  echo "##### $sh MAILPATH"
  PROBE_HOME=$H python3 -I $P/pty.py 0.5 '' $sh -i +m -- 'MAILCHECK=0 MAILPATH=$HOME/m2%got-it-$_:$HOME/m3' 'echo z > $HOME/m2' 'echo w > $HOME/m3' 'MAIL=$HOME/m4' 'echo q > $HOME/m4' 'exit'
  rm -rf $H; mkdir -p $H
  echo "##### $sh MAILCHECK default and 1"
  PROBE_HOME=$H python3 -I $P/pty.py 0.3 '' $sh -i +m -- 'MAIL=$HOME/mbox' 'echo x > $HOME/mbox' ':' 'MAILCHECK=1' 'echo y >> $HOME/mbox' ':' '@1.2' ':' 'exit'
done
