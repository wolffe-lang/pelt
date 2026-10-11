# umask (XCU umask): set, report in octal and with -S, and reach the
# files the shell and its children create.
umask 027
umask
umask -S
: >f1
mkdir d1
(umask 077 && : >f2)
: >f3
ls -ld f1 d1 f2 f3 | cut -c1-10
umask u=rwx,g=rx,o=
umask
umask a+r
umask -S
