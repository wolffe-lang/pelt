# Times out on purpose (tools/reap-witness, pelt#27). The shell writes its
# own pid and those of what it starts to ../../reap.pids (the witness's
# TMPDIR, two levels above the case's working directory): a child, a job
# in a process group of its own (`set -m`), and that job's own child; then
# it blocks opening a FIFO nobody writes, until the harness's timeout.
echo "$$ shell" >> ../../reap.pids
sleep 300 &
echo "$! child" >> ../../reap.pids
set -m
sh -c 'sleep 300 & echo "$! grandchild" >> ../../reap.pids; wait' &
echo "$! job" >> ../../reap.pids
set +m
mkfifo f
: < f
