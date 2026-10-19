(exit 3) & p=$!
wait $p; echo w=$?
jobs
echo end
