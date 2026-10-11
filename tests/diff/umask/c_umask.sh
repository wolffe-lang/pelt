umask 022; umask; umask -S
umask 077; : > f; ls -l f | cut -c1-10
umask 027; sh -c umask
(umask 000; umask); umask
