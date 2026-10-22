# Listing scratch still reports a refused write (pelt#45/#28).
sleep 0.2 &
jobs >/dev/full
echo jobs=$?
wait
