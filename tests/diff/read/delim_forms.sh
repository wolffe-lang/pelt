printf 'axbyc' | { read -d xy v; printf '[%s]\n' "$v"; }
printf 'a\\,b,c' | { read -d , v; printf '[%s]\n' "$v"; }
printf 'a\\\nb,c' | { read -d , v; printf '[%s]\n' "$v"; }
printf 'a\nb,c' | { read -d , v; printf '[%s]\n' "$v"; }
printf 'a b c;' | { read -d ';' x y; printf '[%s][%s]\n' "$x" "$y"; }
printf 'a;b' | { read -d';' x; printf '[%s] %s\n' "$x" "$?"; }
printf 'abc' | { read -d , x; printf '[%s] %s\n' "$x" "$?"; }
printf 'a\\b,' | { read -r -d , x; printf '[%s]\n' "$x"; }
printf 'a\\b\n' | { read -rd '' x; printf '[%s] %s\n' "$x" "$?"; }
printf 'x' | { read -d 2>/dev/null; echo "missing=$?"; }
