printf '[%s]\n' '' "" x ''
set -- '' x ""; echo $#
for w in '' x; do printf '<%s>\n' "$w"; done
v=''; printf '(%s)\n' "$v"
