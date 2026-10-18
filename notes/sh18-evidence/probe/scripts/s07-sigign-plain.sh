grep -E 'SigIgn' /proc/$$/status
sleep 1 &
grep -E 'SigIgn' /proc/$!/status
kill $!
