# umask (XCU umask): an operand that is not a mode, or an option that
# is not -S, fails with status 2 (dash; bash answers 1) and leaves the
# mask alone; umask is a regular built-in, so the shell goes on.
umask 027
for m in u+t o=t , u=rwx,,o=r ,u=rwx u a x 8 0o22 22x +022 'u=r g=r' U=r u=rwxXst; do
    umask "$m" 2>/dev/null
    echo "[$m] st=$? $(umask)"
done
umask -x 2>/dev/null; echo "-x st=$?"
umask -S- 2>/dev/null; echo "-S- st=$?"
umask -w 2>/dev/null; echo "-w st=$? $(umask)"
echo still here
