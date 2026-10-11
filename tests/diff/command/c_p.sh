PATH=/nonexistent
command -p ls / >/dev/null; echo "st=$?"
command -p -v ls | sed 's,.*/,/,'
ls / >/dev/null 2>&1; echo "plain=$?"
