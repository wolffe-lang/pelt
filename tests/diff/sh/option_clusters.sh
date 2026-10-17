../sh -ce 'false; echo no' 2>/dev/null; echo "ce=$?"
../sh -xc 'echo hi' 2>/dev/null; echo "xc=$?"
../sh -nc 'echo no'; echo "nc=$?"
../sh -uc 'echo ${x-ok}'; echo "uc=$?"
../sh -ec -- 'echo "[$0] [$1]"' nm a; echo "ec--=$?"
../sh -eo pipefail -c 'set +o | grep -e errexit -e pipefail'
../sh -fuc 'echo "[$-]"'
