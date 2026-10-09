while read l; do echo "<$l>"; done <<EOF
a
b $HOME
EOF
