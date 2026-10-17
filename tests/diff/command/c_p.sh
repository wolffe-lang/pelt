PATH=/nonexistent
command -p ls / >/dev/null; echo "st=$?"
command -p -v ls | /usr/bin/sed 's,.*/,/,'
command -p -V ls >/dev/null; echo "V=$?"
ls / >/dev/null 2>&1; echo "plain=$?"
