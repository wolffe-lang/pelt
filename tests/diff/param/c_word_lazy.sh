s=v; unset u
echo ${s:-$(echo evaluated >&2)} ${u:+$(echo evaluated >&2)} 2>&1
: ${s:=$(echo evaluated >&2)} 2>&1
i=0; : ${s:-$((i=i+1))}; echo $i
