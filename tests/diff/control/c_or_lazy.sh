true || echo no; echo $?
false || (exit 4); echo $?
false || false || echo third
