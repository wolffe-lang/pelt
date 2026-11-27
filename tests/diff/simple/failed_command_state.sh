x=old; x=new nonexistent_q 2>/dev/null; echo "x=$x st=$?"
y=old; y=new /nonexistent/dir/cmd 2>/dev/null; echo "y=$y"
nonexistent_q $((w=5)) 2>/dev/null; echo "w=$w"
z=old; (z=new : < /nonexistent/file; echo "in z=$z") 2>/dev/null; echo "z=$z st=$?"
k=old; k=new /usr/bin/false; echo "k=$k st=$?"
echo done
