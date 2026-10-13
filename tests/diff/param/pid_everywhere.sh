# `$$` is the shell's process id wherever it is asked: a pipeline
# stage, an asynchronous list, a function, a command substitution all
# answer the invoking shell's (XCU 2.5.2), and a child sees it as its
# parent.
a=$$
echo x | { read l; [ "$a" = "$$" ] && echo pipe-same; }
( [ "$a" = "$$" ] && echo bg-same ) & wait
f() { [ "$a" = "$$" ] && echo fn-same; }; f
[ "$a" = "$(echo $$)" ] && echo cs-same
[ "$(../sh -c 'echo $PPID')" = "$$" ] && echo child-sees-me
echo "${$:+set}"
