x=1; export x
sh -c 'x=2; cd /; umask 077'
echo "$x"; [ "$PWD" != / ] && echo cwd-kept
