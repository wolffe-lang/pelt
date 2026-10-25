# item 7: dash 0.5.13.4 dies (SIGSEGV, status 139) reading $'\342\202\254',
# a three-byte UTF-8 character spelled in octal, before running anything;
# bash and pelt write e2 82 ac
printf %s x$'\342\202'$'\254'y > out1; echo "printf1 st=$?"; od -An -tx1 out1
printf %s $'\342\202\254' > out2; echo "printf2 st=$?"; od -An -tx1 out2
x=$'\342\202\254'; echo "assign st=$?"
echo "$x" | od -An -tx1
