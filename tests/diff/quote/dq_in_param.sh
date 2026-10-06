unset x
echo "${x-'a'}" "${x-"b"}" ${x-'c d'}
