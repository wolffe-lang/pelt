set -a
x=1; : ${y:=2}; : $((z=3)); read r <<E
4
E
for f in 5; do :; done
sh -c 'echo "${x-u} ${y-u} ${z-u} ${r-u} ${f-u}"'
set +a; n=6; sh -c 'echo ${n-unset}'
