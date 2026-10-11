( cd /; exec > /dev/null; echo hidden ); echo visible
[ "$PWD" != / ] && echo cwd-kept
: $(cd /); echo x | cd /; [ "$PWD" != / ] && echo cwd-kept2
