(export 1bad=x; echo "continued $?") 2>/dev/null; echo "st=$?"
export -- ok=1; sh -c 'echo $ok'
