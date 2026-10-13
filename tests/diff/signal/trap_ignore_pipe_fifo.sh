# With SIGPIPE ignored, a write by the shell itself to a pipe nobody
# reads is an error the command reports, not the shell's death; with
# the default the shell dies of it (XCU 2.12; XSH write).
mkfifo f
(
  trap '' PIPE
  /bin/sh -c 'exec <f' &
  exec 3>f
  wait
  echo x >&3 2>/dev/null; echo "ignored: echo=$?"
)
/bin/sh -c 'exec <f' &
../sh -c 'exec 3>f; sleep 1; echo x >&3; echo wrongly-alive' 2>/dev/null
echo "default: $(kill -l $?)"
wait
