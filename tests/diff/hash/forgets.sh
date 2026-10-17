b() { sed 's,.*/,,' | sort | tr '\n' ' '; echo; }
ls / >/dev/null; hash -r; hash | b
ls / >/dev/null; PATH=/usr/bin:/bin; hash | b
ls / >/dev/null; PATH=$PATH; hash | b
PATH=/bin ls / >/dev/null; hash | b
ls / >/dev/null; hash -r cat; echo "r=$?"; hash | b
