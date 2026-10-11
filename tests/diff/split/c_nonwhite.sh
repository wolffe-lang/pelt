IFS=:
x='a::b:'; set -- $x; echo "$# [$1][$2][$3]"
y=':a'; set -- $y; echo "$# [$1][$2]"
z='::'; set -- $z; echo $#
