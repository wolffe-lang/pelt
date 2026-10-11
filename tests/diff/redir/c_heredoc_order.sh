cat <<A; cat <<B
a
A
b
B
cat <<A <<B
ignored
A
used
B
