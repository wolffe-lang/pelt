x=1; y=$(x=2; echo $x); echo $x $y
z=$(cd /; pwd); [ "$PWD" != / ] && echo cwd-kept
