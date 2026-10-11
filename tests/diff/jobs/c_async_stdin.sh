echo data | { cat & wait; echo "[done]"; }
echo data > f; cat < f & wait
