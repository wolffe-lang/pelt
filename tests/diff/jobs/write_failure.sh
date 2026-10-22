# Listing scratch still reports a refused write (pelt#45/#28).
# A read-only descriptor is portable, unlike /dev/full.
: >readonly-input
exec 3<readonly-input
sleep 0.2 &
jobs >&3
echo jobs=$?
wait
exec 3<&-
rm -f readonly-input
