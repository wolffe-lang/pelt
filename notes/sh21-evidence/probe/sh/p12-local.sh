# local, $0, $? on entry, return with no operand
false
command_not_found_handle() { echo "entry st=$? 0=${0##*/}"; local v=in 2>/dev/null; echo "v=${v-}"; true; return; }
v=out; nosuch; echo "st=$? v=$v"
