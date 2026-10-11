hash ls; echo "st=$?"
hash | grep -c ls
hash -r; hash | grep -c ls
hash nonexistent-xyz 2>/dev/null; echo "missing=$?"
