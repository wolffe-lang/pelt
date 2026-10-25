# item 5 (pelt#16): the built-in corners, each measured
command . /nonexistent/file; echo "dot st=$?"
command set -o nosuchoption; echo "set st=$?"
command exec 3</nonexistent; echo "exec st=$?"
command readonly; echo "ro-list st=$?" >/dev/null
export -- ok=1; sh -c 'echo "export ok=$ok"'
export -- ; echo "export-empty st=$?"
printf -- '%s\n' dashdash; echo "printf st=$?"
printf -- ; echo "printf-only-dd st=$?"
(trap 'true; exit' EXIT; exit 7); echo "exit-in-trap st=$?"
(trap 'false; exit' EXIT; true); echo "exit-in-trap2 st=$?"
(trap 'exit 4' EXIT; exit 7); echo "exit-n-in-trap st=$?"
readonly a='x y' b
readonly -p | grep -E ' (a|b)(=|$)'
pwd -x; echo "pwd-x st=$?"
pwd -LP >/dev/null; echo "pwd-LP st=$?"
cd -e . ; echo "cd-e st=$?"
cd -P -e . ; echo "cd-Pe st=$?"
echo survived
