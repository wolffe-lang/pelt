# item 4: a built-in's write to a closed standard output, and a bad option
echo hi >&-; echo "echo-closed1 st=$?"
printf x >&-; echo "printf-closed1 st=$?"
pwd >&-; echo "pwd-closed1 st=$?"
(trap -xy 'echo t' INT); echo "trap-xy st=$?"
(trap -- -x INT); echo "trap-dd st=$?"
