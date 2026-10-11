f() { x=inside; }; echo "${x-unset}"; f; echo "$x"
