i=0; while [ $i -lt 300000 ]; do i=$((i+1)); done
times | sed -n 1p | grep -q '^0m0[.,]0*s ' && echo zero || echo nonzero
