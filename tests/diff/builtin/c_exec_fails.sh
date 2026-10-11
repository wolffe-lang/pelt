(exec nonexistent-xyz; echo no) 2>/dev/null; echo "st=$?"
: > noexec; (exec ./noexec; echo no) 2>/dev/null; echo "st=$?"
