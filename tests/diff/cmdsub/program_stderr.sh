x=$(ls ./nosuch_z 2>/dev/null)
echo "[$x]"
y=$(ls ./nosuch_z 2>&1 | wc -l)
echo $y
