printf 'echo "ld [$0] [$1]"\n' > s3
../sh - s3 y; echo "st=$?"
echo 'echo "[$1] $#"' | ../sh -s - x
echo 'echo "[$1] $#"' | ../sh -s -- -x y
