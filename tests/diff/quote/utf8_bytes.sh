# Bytes above 0x7f that form UTF-8 are data like any other: in an
# argument to a program, in a file name, in what `read` reads, in a
# command substitution, in a here-document and in a pattern (XCU 2.2,
# 2.6.3, 2.7.4, read). quote/c_s_high_bytes asks the same of a byte
# that is not UTF-8 too, which waits on wolf byte strings (W06).
e=$(printf '\303\251')
printf '%s' "$e" | od -An -tx1 | tr -d '[:space:]'; echo
/usr/bin/env printf '%s' "caf$e" | od -An -tx1 | tr -d '[:space:]'; echo
/usr/bin/env printf '%s' caf"$e"s 'caf'"$e"'s' | od -An -tx1 | tr -d '[:space:]'; echo
printf 'F\305\221t\n' | while read -r w; do printf '%s' "$w" | od -An -tx1 | tr -d '[:space:]'; echo; done
printf 'F\305\221t\n' | while read -r w; do /usr/bin/env printf '%s' "$w" | od -An -tx1 | tr -d '[:space:]'; echo; done
cat <<E | od -An -tx1 | tr -d '[:space:]'
x${e}y
E
echo
: >"n$e"
ls | od -An -tx1 | tr -d '[:space:]'; echo
for f in n*; do /usr/bin/env printf '%s' "$f" | od -An -tx1 | tr -d '[:space:]'; echo; done
case "caf$e" in caf"$e") echo "pattern: quoted" ;; *) echo "pattern: no" ;; esac
case "caf$e" in caf?*) echo "pattern: wildcard" ;; *) echo "pattern: no" ;; esac
x="a${e}b"; echo "${x#a}" | od -An -tx1 | tr -d '[:space:]'; echo
echo "${#e}"
