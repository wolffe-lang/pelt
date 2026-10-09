true | false
echo $?
false | true
echo $?
false | sh -c 'exit 7'
echo $?
