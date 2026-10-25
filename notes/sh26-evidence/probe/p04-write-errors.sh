# item 4 (pelt#28): a built-in's failed write, not EPIPE
echo hi >&3; echo "echo-closed st=$?"
printf 'x\n' >&3; echo "printf-closed st=$?"
echo hi >/dev/full; echo "echo-full st=$?"
printf 'x\n' >/dev/full; echo "printf-full st=$?"
pwd >/dev/full; echo "pwd-full st=$?"
exec 4</dev/null; echo hi >&4; echo "echo-rdonly st=$?"
echo end
