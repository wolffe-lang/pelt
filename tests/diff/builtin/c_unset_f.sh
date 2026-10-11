f=var; f() { echo func; }
unset -f f; echo "$f"; f 2>/dev/null; echo "st=$?"
g() { :; }; g=var; unset g; echo "${g-var-unset}"; g; echo "func-st=$?"
