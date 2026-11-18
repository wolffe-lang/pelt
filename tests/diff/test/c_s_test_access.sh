# test -r/-w/-x ask whether THIS process may read, write or execute or
# search the file (XCU test), and -L/-h whether it is a symbolic link;
# -ef whether two names are one file (POSIX.1-2024). Every name is a
# file the case makes: a system path's type varies by host (pelt#138:
# /usr/bin/env is a symbolic link on some, a program on others).
: >plain
chmod 644 plain
cp /bin/sh prog 2>/dev/null || : >prog
chmod 755 prog
: >secret
chmod 000 secret
: >ro
chmod 444 ro
cp prog progro
chmod 555 progro
mkdir dir
ln -s plain link
ln -s prog proglink
ln plain hard
for f in plain prog secret ro dir link progro proglink /nonexistent; do
    r=n w=n x=n l=n
    test -r "$f" && r=y
    test -w "$f" && w=y
    test -x "$f" && x=y
    test -L "$f" && l=y
    [ -h "$f" ] || l="$l-"
    echo "$f r=$r w=$w x=$x L=$l"
done
test plain -ef hard && echo "ef: same file"
test plain -ef prog || echo "ef: different files"
test -f proglink && test -x proglink && echo "proglink is a program"
chmod 600 secret
