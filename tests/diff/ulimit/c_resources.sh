ulimit -S -n 64; ulimit -n; ulimit -S -n
ulimit -H -n >/dev/null; echo "H=$?"
ulimit -c 0; ulimit -c
ulimit -a >/dev/null; echo "a=$?"
ulimit -s >/dev/null; echo "s=$?"; ulimit -t >/dev/null; echo "t=$?"; ulimit -d >/dev/null; echo "d=$?"; ulimit -v >/dev/null; echo "v=$?"
