# item 5: which subshells list the shell's traps (trap with no operand)
trap 'echo i' INT
trap '' QUIT
echo "pipe:"; trap | cat
echo "sub:"; (trap)
echo "cmdsub:"; echo "$(trap)"
echo "cmdsub2:"; echo "$(trap; :)"
echo "brace pipe:"; { trap; } | cat
