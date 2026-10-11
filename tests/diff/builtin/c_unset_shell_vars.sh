unset IFS; x='a b'; set -- $x; echo $#
(unset PATH; echo builtin-still-works; ls >/dev/null 2>&1; echo "ls=$?") | sed 's/ls=0/ls=found-by-default-path/'
unset HOME; echo "${HOME-unset}"
unset LINENO PPID 2>/dev/null; echo survived
