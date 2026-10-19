(exit 5) &
sleep 0.2
p=$(jobs -p)
echo "listed=$(printf '%s\n' "$p" | grep -c .)"
(exit 6) &
sleep 0.2
wait $p; echo "first-after-next=$?"
