(. ./nonexistent; echo no) 2>/dev/null; echo "st=$?"
(. nonexistent-in-path; echo no) 2>/dev/null; echo "st=$?"
