a=1; export b=2; c=3 sh -c 'echo "${a-unset} ${b-unset} ${c-unset}"'
