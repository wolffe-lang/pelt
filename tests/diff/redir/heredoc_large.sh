i=0
while [ $i -lt 1500 ]; do echo "line $i of the body"; i=$((i+1)); done >f
x=$(cat f)
cat <<EOF | wc -l | tr -d ' '
$x
EOF
while read a b c; do n=$b; done <<EOF
$x
EOF
echo $n
