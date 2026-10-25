# pelt#61, XCU 2.8.2: why a slashed command cannot run, in dash's words
# (the part after the shell's own prefix), and the status: 127 when the
# name does not resolve to a file, 126 when it does and cannot be run
why() { { "$@"; echo "st=$?"; } 2>&1 | sed "s|^.*$1: ||"; }
echo x > f; why ./f/x
ln -s loop1 loop2; ln -s loop2 loop1; why ./loop1
ln -s nowhere dangle; why ./dangle
why ./$(printf '%0300d' 0)
mkdir d; why ./d
echo 'echo hi' > nox; why ./nox
why ./nope
why ../nonexistent/x
printf '#!/nonexistent/interp\necho ran\n' > badi; chmod +x badi; why ./badi
mkdir -p locked/sub; chmod 0 locked; why ./locked/sub; chmod 755 locked
ex() { { (exec "$@"); echo "st=$?"; } 2>&1 | sed "s|^.*exec: $1: |exec: |"; }
ex ./f/x
ex ./loop1
ex ./d
ex ./nox
ex ./nope
