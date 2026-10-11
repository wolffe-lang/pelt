x=1; { x=2; cd /; } & wait; echo "$x"; [ "$PWD" != / ] && echo cwd-kept
