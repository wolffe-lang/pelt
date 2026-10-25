# run by hand: dash's MAIL rule with explicit modification times (pty.py)
P=/home/mfwolffe/lanes/sh26/probe
H=$HOME/mailh
for sh in /usr/bin/dash; do
 for mc in 0 100 unset; do
  rm -rf $H; mkdir -p $H; echo pre > $H/mbox; touch -d @1000 $H/mbox
  if [ $mc = unset ]; then e="MAIL=$H/mbox"; else e="MAIL=$H/mbox MAILCHECK=$mc"; fi
  echo "##### $sh MAILCHECK=$mc"
  PROBE_HOME=$H python3 -I $P/pty.py 0.15 "$e" $sh -i +m -- 'touch -d @2000 $HOME/mbox' 'touch -d @3000 $HOME/mbox' 'touch -d @4000 $HOME/mbox' ': > $HOME/mbox; touch -d @5000 $HOME/mbox' 'echo x >$HOME/mbox; touch -d @5000 $HOME/mbox' 'echo xy >$HOME/mbox; touch -d @5000 $HOME/mbox' 'touch -d @6000 $HOME/mbox' '@1.1' 'touch -d @7000 $HOME/mbox' 'exit'
 done
done
