readonly r=1
echo x | { read r 2>/dev/null; echo "st=$?"; } 2>/dev/null
echo x | { read 1bad 2>/dev/null; echo "st=$?"; } 2>/dev/null
