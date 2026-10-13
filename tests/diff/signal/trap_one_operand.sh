# A lone operand that names a condition resets it (dash; XCU `trap`
# says so for an unsigned integer).
trap 'echo x' USR1; trap USR1; trap; echo "name=$?"
trap 'echo x' USR1 USR2; trap usr1; trap; trap - USR2
trap 'echo x' HUP; trap 1; trap; echo "number=$?"
trap 'echo x' EXIT; trap EXIT; trap; echo "exit=$?"
