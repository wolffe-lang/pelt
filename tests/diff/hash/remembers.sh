b() { sed 's,.*/,,' | sort | tr '\n' ' '; echo; }
hash; echo "empty=$?"
ls / >/dev/null; cat </dev/null; hash | b
hash -r; hash sort; echo "st=$?"; hash | b
hash echo cd; echo "builtin=$?"; f() { :; }; hash f; echo "function=$?"; hash /usr/bin/ls; echo "slash=$?"; hash | b
hash wc nonexistent-xyz tr 2>/dev/null; echo "missing=$?"; hash | b
hash -- head; hash | b
command -v uniq >/dev/null; type cut >/dev/null; hash | b
ls / | cat >/dev/null; hash | b
