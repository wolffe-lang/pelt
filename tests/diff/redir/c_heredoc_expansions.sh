x=val
cat <<E
$x ${x} $(echo cmd) `echo bq` $((1+2)) ~ * 'q' "dq"
E
