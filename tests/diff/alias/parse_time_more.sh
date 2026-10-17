alias q='echo Q'
echo "$(q hi)"
echo "`q bq`"
alias r='echo R'; eval 'r ev'
printf 'q dotted\n' > d1
. ./d1
printf 'alias s="echo S"\ns inside\n' > d2
. ./d2
s after
