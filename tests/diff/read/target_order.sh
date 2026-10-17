readonly r=1
echo x y | { read a r; echo "st=$? a=$a"; } 2>/dev/null
echo x y | { read r b; echo "st=$? b=[$b]"; } 2>/dev/null
echo x y | { read 1bad b; echo "st=$? b=[$b]"; } 2>/dev/null
echo x | { read a-b; echo "st=$?"; } 2>/dev/null
echo x | { read r; echo "after"; } 2>/dev/null; echo "outer=$? r=$r"
