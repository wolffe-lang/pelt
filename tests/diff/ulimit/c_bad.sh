(ulimit -H -n 32; ulimit -H -n 64 2>/dev/null; echo "raise=$?") | sed 's/raise=[1-9][0-9]*/raise=failed/'
ulimit -n abc 2>/dev/null; echo "st=$?"
