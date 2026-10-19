i=0
while [ $i -lt 5000 ]; do true & i=$((i+1)); done
sleep 0.3
jobs > "${TMPDIR:-/tmp}/w09.$$"
echo "jobs=$(grep -c Done "${TMPDIR:-/tmp}/w09.$$")"
rm -f "${TMPDIR:-/tmp}/w09.$$"
