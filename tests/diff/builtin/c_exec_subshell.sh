(exec sh -c 'exit 4'); echo "st=$?"
x=$(exec echo from-exec); echo "$x"
echo survived
