unset u
echo "${u:-a  'b'  *}"
echo "${u:-a\}b}"
echo "${u:-$HOME}"
