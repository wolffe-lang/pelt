printf 'a\\ b c\\\nd\n' | { read x y; echo "[$x][$y]"; }
printf 'a\\ b c\\\nd\n' | { read -r x y; echo "[$x][$y]"; read -r z; echo "[$z]"; }
printf 'a\\tb\n' | { read x; echo "[$x]"; }
