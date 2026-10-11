mkdir d; cd d; sh -c 'pwd' | sed 's,.*/,,'
exec 3>../f3; sh -c 'echo via-3 >&3'; exec 3>&-; cat ../f3
