# The side not evaluated by `&&`, `||` or `?:` changes nothing and
# raises nothing, nested two deep: no assignment and no division by zero.
x=1
echo $((0 && (1 || (x=5)))) $x $((1 || (0 && (x=6)))) $x
echo $((0 ? (x=7) : 1 ? 2 : (x=8))) $x $((1 ? (0 ? (x=9) : 3) : (x=10))) $x
echo $((0 && 1/0)) $((1 || 1%0)) $((1 ? 4 : 1/0)) $((0 ? 1/0 : 5)) $((0 && (1 ? 1/0 : 2)))
