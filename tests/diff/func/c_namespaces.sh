x=var; x() { echo func; }
echo $x; x
unset x; x; unset -f x; x 2>/dev/null; echo "st=$?"
