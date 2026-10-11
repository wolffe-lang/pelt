readonly r=1
(echo x | { read r; echo "read-st=$?"; }) 2>/dev/null
(for r in a b; do echo no; done; echo no) 2>/dev/null; echo "for=$?"
(: $((r=5)); echo no) 2>/dev/null; echo "arith=$?"
(: ${r:=5}; echo "default-kept $r") 2>/dev/null
(getopts a r -a; echo "getopts-st=$?") 2>/dev/null; echo "getopts=$?"
echo "$r"
