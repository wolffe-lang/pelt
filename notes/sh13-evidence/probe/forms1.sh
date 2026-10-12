# sh13 probe: umask forms under dash and bash --posix, black-box (notes/sh13-the-umask.md)
for m in 0 7777 1777 0777 777 8 00022 000000022 '' 0o22 22x -022 +022; do
  umask 022; umask "$m" 2>/dev/null; st=$?; printf '%s -> st=%s now=%s\n' "[$m]" "$st" "$(umask)"
done
umask 022; umask -- 027; echo "dashdash st=$? $(umask)"
umask 022; out=$(umask -S 027); echo "S-with-op st=$? out=[$out] now=$(umask)"
umask 022; umask -x 2>/dev/null; echo "bad-opt st=$?"
umask 022; umask 027 033 2>/dev/null; echo "two-ops st=$? now=$(umask)"
umask 022; umask -S -S 2>/dev/null; echo "SS st=$?"
umask 022; umask -- ; echo "dd-only st=$?"
umask 022; umask -S --; echo "S-dd st=$?"
for m in +w -w =r a= u=g g=u-w o+X u+s +t g+t u=rwx,g=rx,o= ug+rw a-rwx u=r,u+w 'u=rwx,,o=r' u =r 'u=rwx,' ',u=rwx' 'u=rw,g=u' 'g=o' 'go=u' 'u+x,g-x' 'a+X' 'u=rwxs' 'o=t' 'au=r' 'u+r+w' 'u+r-w' 'u=+r' 'u==r' 'g+u' 'u=r g=r' 'U=r' 'u=X' 'u+X' 'ugoa-x'; do
  umask 027; umask "$m" 2>/dev/null; st=$?; printf '%s -> st=%s now=%s S=%s\n' "[$m]" "$st" "$(umask)" "$(umask -S)"
done
