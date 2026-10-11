[ a = a -a b = b ]; echo $?; [ a = a -a b = c ]; echo $?; [ a = b -o b = b ]; echo $?
[ \( a = a \) ]; echo $?; [ \( a = b \) -o \( c = c \) ]; echo $?; [ ! \( a = b \) ]; echo $?
