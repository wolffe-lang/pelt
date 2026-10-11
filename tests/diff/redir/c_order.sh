{ echo out; echo err >&2; } >o 2>&1; cat o
{ echo out; echo err >&2; } 2>&1 >o2 | cat; cat o2
