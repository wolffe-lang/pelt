# XCU 2.9.1.4: a file the kernel will not run (ENOEXEC) is run by a
# shell invoked with its name as the operand. dash 0.5.13.4 invokes
# /bin/sh, the plain command and exec alike, and hands it a binary file
# too (the bypass is optional): the answer is whatever this host's
# /bin/sh answers, so the case compares with /bin/sh's own answer
# (sh26, R-sh26-1).
printf '\0\0\0\0binary\n' > bin; chmod +x bin
./bin >/dev/null 2>&1; a=$?
/bin/sh ./bin >/dev/null 2>&1; b=$?
[ "$a" = "$b" ] && echo "plain: as /bin/sh" || echo "plain: $a, /bin/sh $b"
(exec ./bin) >/dev/null 2>&1; a=$?
[ "$a" = "$b" ] && echo "exec: as /bin/sh" || echo "exec: $a, /bin/sh $b"
