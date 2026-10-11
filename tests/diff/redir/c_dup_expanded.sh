n=2; d=-
(echo via-var >&$n) 2>&1
exec 3>f; exec 3>&$d; (echo x >&3) 2>/dev/null; echo "st=$?"
