# umask in a subshell (XCU 2.13): a ( ), a command substitution, a
# pipeline stage and an asynchronous list each change only their own
# mask; a function and a redirected umask change the shell's.
umask 022
(umask 077); umask
x=$(umask 077; umask); echo "$x"; umask
umask 077 | cat; umask
{ umask 077; } | cat; umask
umask 077 & wait; umask
(umask 027; (umask 077); umask); umask
f() { umask 077; }; f; umask
umask 022; umask 066 >/dev/null; umask
