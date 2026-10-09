i=0
while [ $i -lt 3000 ]; do echo "line $i"; i=$((i+1)); done | wc -l | tr -d ' '
