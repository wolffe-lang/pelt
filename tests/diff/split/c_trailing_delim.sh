IFS=:
x='a:b:'; set -- $x; echo $#
y='a:b::'; set -- $y; echo $#
