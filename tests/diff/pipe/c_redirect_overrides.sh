echo to-file | cat > f; cat f
echo hidden > g | cat; echo "[$(cat g)]"
echo a | cat < /dev/null; echo "st=$?"
