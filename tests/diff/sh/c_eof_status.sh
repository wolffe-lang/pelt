printf 'false\n' | ../sh; echo $?
printf 'true\n(exit 5)' | ../sh; echo $?
