printf '%d\n' abc 2>/dev/null; echo "st=$?"
printf '%d\n' 12x 2>/dev/null; echo "st=$?"
printf '%d\n' '' 2>/dev/null; echo "st=$?"
for n in +12x -12x 0x12x 078 ' 12x' + - 0x 08x -0x1fx; do
    printf '%d\n' "$n" 2>/dev/null; echo "st=$?"
done
