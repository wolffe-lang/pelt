# umask (XCU umask): -S with an operand sets the mask and writes
# nothing (dash; bash writes it); -- ends the options; only the first
# operand is read; the output can be piped.
umask 022; umask -S 027; echo "st=$?"; umask
umask 022; umask -- 027; umask
umask 022; umask 027 033; umask
umask -SS; umask -S --
umask | cat; umask -S | cat
