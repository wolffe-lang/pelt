# /dev/full fails writes without a SIGPIPE (pelt#28).
echo data >/dev/full
echo echo=$?
printf '%s\n' data >/dev/full
echo printf=$?
