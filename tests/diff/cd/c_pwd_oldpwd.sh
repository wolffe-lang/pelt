mkdir a; start=$PWD; cd a
[ "$OLDPWD" = "$start" ] && echo oldpwd; [ "$PWD" = "$start/a" ] && echo pwd
