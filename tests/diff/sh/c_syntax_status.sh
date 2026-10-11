../sh -c 'if then' 2>/dev/null; s=$?; [ $s -ge 1 ] && [ $s -le 125 ] && echo in-range
echo 'echo ok
)' > bad; ../sh bad 2>/dev/null; s=$?; [ $s -ge 1 ] && [ $s -le 125 ] && echo in-range
