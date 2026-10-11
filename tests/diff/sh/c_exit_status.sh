printf '\n# c\n\n' > empty; ../sh empty; echo $?
echo '(exit 9)' > nine; ../sh nine; echo $?
echo 'exit 4; echo no' > four; ../sh four; echo $?
