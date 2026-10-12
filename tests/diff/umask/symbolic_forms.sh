# umask (XCU umask; chmod's symbolic_mode): the forms the census cases
# do not reach. An empty who is all three classes; X and the copy
# letters read the permissions as they were before the operand; s
# changes nothing; one trailing comma is accepted; an octal operand
# keeps its low nine bits.
umask 027; umask +w; umask
umask 027; umask =r; umask
umask 027; umask u=g; umask
umask 027; umask g=u-w; umask
umask 027; umask o+X; umask
umask 777; umask u+x,o+X; umask
umask 777; umask a=rwx,o-X; umask
umask 077; umask g=rwx,o=g; umask
umask 027; umask u+s; umask
umask 027; umask u=r,u+w; umask
umask 027; umask u+r-w; umask
umask 027; umask u=+r; umask
umask 027; umask u=rwx,; umask
umask 027; umask ''; umask
umask 027; umask -; umask
umask 027; umask -- -w; umask
umask 0; umask a-X; umask -S
umask 027; umask a=; umask -S
umask 027; umask 7777; umask
umask 027; umask 01000; umask
umask 027; umask 000000022; umask
