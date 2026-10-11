printf 'no-newline' | { read x; echo "$? [$x]"; }
printf '' | { read x; echo "$? [$x]"; }
printf 'a\nb\n' | { while read l; do echo "<$l>"; done; echo "end=$?"; }
