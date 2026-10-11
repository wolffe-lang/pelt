unset u
echo ${u:-a}b} ${u:-'}'} ${u:-"}"} ${u:-\}} ${u:-$(echo '}')} ${u:-${u:-x}y}
