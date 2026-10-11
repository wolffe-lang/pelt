false && echo foo || echo bar
true || echo foo && echo bar
false || false && echo no; echo $?
true && false || true && echo yes
