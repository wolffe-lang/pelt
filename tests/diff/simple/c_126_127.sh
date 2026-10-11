nonexistent-xyz 2>/dev/null; echo $?
./nonexistent 2>/dev/null; echo $?
: > noexec; ./noexec 2>/dev/null; echo $?
mkdir dir; ./dir 2>/dev/null; echo $?
