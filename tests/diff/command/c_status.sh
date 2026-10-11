command sh -c 'exit 5'; echo $?
command nonexistent-xyz 2>/dev/null; echo $?
: > noexec; command ./noexec 2>/dev/null; echo $?
command -- echo dashdash
