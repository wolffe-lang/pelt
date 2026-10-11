trap 'echo "x=$x st=$?"' EXIT
x=1; (exit 4)
