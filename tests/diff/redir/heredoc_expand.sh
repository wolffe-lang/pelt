x=1
cat <<EOF
$x \$x "q" \\ \" $(echo c) $((1+2)) `echo d`
next \
line
EOF
