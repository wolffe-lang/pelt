echo 'echo "$# $1 $2"' | ../sh -s a b
echo 'echo "implied $#"' | ../sh
echo 'echo dash-operand $1' | ../sh -s - x
