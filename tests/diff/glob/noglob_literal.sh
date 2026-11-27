touch a b
set -f
printf '[%s]\n' * a? [ab]
for w in * ?; do printf '<%s>\n' "$w"; done
set +f
printf '(%s)\n' [ab] a?
