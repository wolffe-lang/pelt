(echo $((1 +)); echo no) 2>/dev/null; echo "st=$?"
(x=abc; abc=; echo $((1 + 2x)); echo no) 2>/dev/null; echo "st=$?"
(echo $((1/0)); echo no) 2>/dev/null; echo "st=$?"
(echo $((1%0)); echo no) 2>/dev/null; echo "st=$?"
