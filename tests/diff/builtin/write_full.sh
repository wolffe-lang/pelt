# A read-only descriptor refuses writes without SIGPIPE on Unix.
# Unlike /dev/full, this control is available on macOS too (pelt#28).
: >readonly-input
exec 3<readonly-input
echo data >&3
echo echo=$?
printf '%s\n' data >&3
echo printf=$?
exec 3<&-
rm -f readonly-input
