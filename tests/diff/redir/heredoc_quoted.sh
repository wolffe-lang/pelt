x=1
cat <<'EOF'
$x $(nope) \$x
EOF
cat <<"E2"
$x
E2
cat <<E\3
$x
E3
