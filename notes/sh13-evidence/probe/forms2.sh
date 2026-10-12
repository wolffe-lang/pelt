# sh13 probe: umask forms under dash and bash --posix, black-box (notes/sh13-the-umask.md)
umask 027; umask ''; echo "empty st=$? now=$(umask)"
umask 027; x=$(umask ''); echo "empty-out=[$x]"
for start in 027 077 777 666 0; do
for m in u+t a+t ug+t o+t u=t +s a+s =s u=X a=X o+X u-X a-X go=X 'u=rwx,o=X' 'u-x,o=X' 'o=X,u-x' u+w,u-w 'u=rw-x' 'a=rwx,o-X' 'u=rwxXst' 'u=' 'u-' 'u+' '=' '+' '-' 'a' ',' 'u=r,' 'u=r,,' 'u+rr'; do
  umask $start; umask -- "$m" 2>/dev/null; st=$?; printf '%s %s -> st=%s now=%s\n' "$start" "[$m]" "$st" "$(umask)"
done
done
