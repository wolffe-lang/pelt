# test -r/-w/-x ask whether THIS process may read, write or execute or
# search the file (XCU test), and -L/-h whether it is a symbolic link;
# -ef whether two names are one file (POSIX.1-2024).
: >plain
chmod 644 plain
cp /bin/sh prog 2>/dev/null || : >prog
chmod 755 prog
: >secret
chmod 000 secret
: >ro
chmod 444 ro
mkdir dir
ln -s plain link
ln plain hard
for f in plain prog secret ro dir link /usr/bin/env /nonexistent; do
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
test -f /usr/bin/env && test -x /usr/bin/env && echo "env is a program"
chmod 600 secret
