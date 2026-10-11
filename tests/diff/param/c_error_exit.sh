s=v; echo "${s:?no}"
n=; echo "${n?fine}ok"
(unset u; : ${u:?message here}; echo not-reached) 2>&1 | grep -c 'message here'
unset u; : ${u?}; echo not-reached
