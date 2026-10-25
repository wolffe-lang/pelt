# XCU 2.9.1.4: an executable text file with no #! line runs as a shell
# script, by name with a slash, through PATH, and after exec ($0 is the
# name it was run by; dash: /bin/sh NAME ARG..., R-sh26-1)
printf 'echo "ran ${0##*/} [$1] [$2] $#"\nexit 3\n' > t; chmod +x t
./t a 'b c'; echo "st=$?"
PATH=$PWD:$PATH t d; echo "st=$?"
(exec ./t e); echo "st=$?"
x=$(./t f); echo "$x st=$?"
