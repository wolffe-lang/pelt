# A declaration utility is recognised after its name is expanded, and
# after `command` and its options: its assignment-shaped operands are
# not split or globbed, and take tilde after `=` (XCU 2.9.1.1). `local`
# is dash's, and behaves the same. A word that is not assignment-shaped
# (`"g=$y"`, quoted) and any other command's operands expand as usual.
y='p q'; HOME=/hh
f() { local l=$y; echo "[$l]"; }; f
command -p export c=$y; echo "[$c]"
e=export; $e d=$y; echo "[$d]"
export "g=$y" h=~/x; echo "[$g] [$h]"
export i=*; echo "[$i]"
echo export j=$y
