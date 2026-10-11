set -u
(echo $((u + 1)); echo no) 2>/dev/null; [ $? -ne 0 ] && echo failed
