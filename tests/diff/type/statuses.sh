f() { :; }
type f >/dev/null; echo "f=$?"; type exit >/dev/null; echo "exit=$?"; type if >/dev/null; echo "if=$?"
type nonexistent-xyz 2>/dev/null | wc -l | tr -d ' '; type nonexistent-xyz >/dev/null 2>&1; echo "missing=$?"
type ls nonexistent-xyz cd 2>/dev/null | wc -l | tr -d ' '; type ls nonexistent-xyz cd >/dev/null 2>&1; echo "many=$?"
type /usr/bin/env | grep -c /usr/bin/env; type ./nope >/dev/null; echo "nope=$?"
: > plain; type ./plain >/dev/null; echo "plain=$?"
type; echo "none=$?"; type -- cd >/dev/null; echo "dashdash=$?"; type -p ls >/dev/null 2>&1; echo "opt=$?"
ls / >/dev/null; type ls | grep -c ls
