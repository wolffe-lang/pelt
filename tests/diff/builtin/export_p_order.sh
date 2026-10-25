# pelt#16: export -p and readonly -p list every marked name in one sorted
# list, a name with no value without =; -- ends the options
readonly aa; readonly zz=1; readonly mm='x y'
readonly -p | grep -E ' (aa|mm|zz)(=|$)'
export AA; export ZZ=1; export MM='x y'
export -p | grep -E ' (AA|MM|ZZ)(=|$)'
export -- QQ=2; export -p -- | grep QQ
readonly -- RR=3; readonly -p | grep RR
export -- | grep -E ' (AA|QQ)(=|$)'
