x=1; export x; unset x; echo "${x-unset}"; x=2; sh -c 'echo ${x-not-exported}'
y=1; unset -v y; echo "${y-unset}"
a=1 b=2; unset a b; echo "${a-u}${b-u}"
unset never_set_xyz; echo "st=$?"
