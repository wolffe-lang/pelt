[ a \< b ] && echo lt
[ b \> a ] && echo gt
[ B \< a ]; echo $?
test abc \< abd; echo $?
