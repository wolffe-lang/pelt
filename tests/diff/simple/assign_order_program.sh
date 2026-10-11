# Assignments before a command are expanded in order, each seeing the
# ones before it (XCU 2.9.1.1): `y=$x` after `x=3` hands the program
# y=3. Before a program they leave the shell's own variables alone;
# before a special built-in they stay.
x=1
x=3 y=$x env | grep '^[xy]=' | sort
echo "after a program: x=$x y=${y-unset}"
x=3 y=$x :
echo "after a special built-in: x=$x y=$y"
