echo "[${!:-unset}]"
true &
echo "[${!:+set}]"
wait
