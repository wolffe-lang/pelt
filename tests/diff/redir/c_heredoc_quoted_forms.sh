x=val
cat <<'E'
$x 1
E
cat <<"E"
$x 2
E
cat <<\E
$x 3
E
cat <<E"O"F
$x 4
EOF
