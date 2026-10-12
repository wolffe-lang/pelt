# umask (XCU umask): the mask reaches the files the shell creates, the
# programs it starts (touch, mkdir, another shell) and the program exec
# becomes; a shell that starts with a mask and changes it only in a
# subshell keeps the one it started with.
umask 077
: >a; touch b; mkdir c; sh -c ': >d'; ../sh -c ': >e'
ls -ld a b c d e | cut -c1-10
umask 027; ../sh -c '(umask 077); umask'
umask 027; ../sh -c 'x=$(umask 002); umask'
umask 027; ../sh -c 'umask 077; exec ../sh -c umask'
umask 027; x=$(../sh -c 'umask 002; umask'); echo "$x"; umask
