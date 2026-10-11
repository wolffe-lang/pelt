x=$(exit 3) y=$(exit 5); echo $?
false; x=1; echo $?
false; $(exit 0); echo $?
$(exit 9); echo $?
