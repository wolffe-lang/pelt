# item 5: the order readonly -p and export -p list set and unset names
readonly aa; readonly zz=1; readonly mm='x y'
readonly -p | grep -E ' (aa|mm|zz)(=|$)'
export AA; export ZZ=1; export MM='x y'
export -p | grep -E ' (AA|MM|ZZ)(=|$)'
export -- QQ=2; export -p -- | grep QQ; echo "st=$?"
readonly -- RR=3; readonly -p | grep RR
export --; echo "export-dd st=$?"
