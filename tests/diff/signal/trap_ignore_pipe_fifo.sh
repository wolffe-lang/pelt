# With SIGPIPE ignored, a write by the shell itself to a pipe nobody
# reads is an error the command reports, not the shell's death; with
# the default the shell dies of it (XCU 2.12; XSH write). The reader
# holds the FIFO open until the writer says it has opened it (and gives
# up after five seconds, so nothing is left behind if the writer never
# comes), then leaves.
mkfifo f
reader='exec 3<>f; i=0; while [ ! -e opened ] && [ $i -lt 50 ]; do sleep 0.1; i=$((i+1)); done'
(
  trap '' PIPE
  /bin/sh -c "$reader" &
  exec 3>f; : > opened
  wait
  echo x >&3 2>/dev/null; echo "ignored: echo=$?"
)
rm -f opened
/bin/sh -c "$reader" &
../sh -c 'exec 3>f; : > opened; sleep 1; echo x >&3; echo wrongly-alive' 2>/dev/null
echo "default: $(kill -l $?)"
wait
