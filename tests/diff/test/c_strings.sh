[ abc = abc ]; echo $?; [ abc = abd ]; echo $?; [ abc != abd ]; echo $?
[ a \< b ]; echo $?; [ b \< a ]; echo $?; [ b \> a ]; echo $?; [ a \> a ]; echo $?
[ '' = '' ]; echo $?; [ ' a' = a ]; echo $?
