{ echo 1; echo 2; echo 3; } | while read n; do echo "n=$n"; done | sed 's/^/>/'
