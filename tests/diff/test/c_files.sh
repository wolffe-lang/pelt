: > empty; echo x > full; mkdir dir; ln -s full lnk; ln -s nowhere dangling; chmod 644 full
for p in -e -f -d -s -L -h -r -w -x; do
  for f in empty full dir lnk dangling missing; do [ $p $f ] && printf '%s:%s ' $p $f; done; echo
done
