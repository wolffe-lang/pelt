# Bytes above 0x7f are data: in an argument to a program, in a file
# name, in what `read` reads, in a command substitution and in a
# here-document (XCU 2.2, 2.6.3, 2.7.4, read; a shell passes on any
# byte but NUL). The hex dumps are the proof; the script itself is
# ASCII.
e=$(printf '\303\251')
printf '%s' "$e" | od -An -tx1 | tr -d '[:space:]'; echo
/usr/bin/env printf '%s' "caf$e" | od -An -tx1 | tr -d '[:space:]'; echo
printf 'F\305\221t\n' | while read -r w; do printf '%s' "$w" | od -An -tx1 | tr -d '[:space:]'; echo; done
printf 'F\305\221t\n' | while read -r w; do /usr/bin/env printf '%s' "$w" | od -An -tx1 | tr -d '[:space:]'; echo; done
cat <<E | od -An -tx1 | tr -d '[:space:]'
x${e}y
E
echo
: >"n$e"
ls | od -An -tx1 | tr -d '[:space:]'; echo
for f in n*; do /usr/bin/env printf '%s' "$f" | od -An -tx1 | tr -d '[:space:]'; echo; done
l=$(printf 'a\377b')
/usr/bin/env printf '%s' "$l" | od -An -tx1 | tr -d '[:space:]'; echo
echo "${#e}"
