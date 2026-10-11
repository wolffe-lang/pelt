env 'a.b=1' 'ok_1=2' ../sh -c 'echo "${ok_1}"; set | grep -c "^a\.b="'
