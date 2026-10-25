# item 3 (pelt#6): -v with -c strings and script operands, stderr shown
exec 2>&1
../sh -v -c 'echo a
echo b'
echo "st=$?"
../sh -c 'set -v
echo c
echo d'
echo "st=$?"
../sh -c 'set -v; echo e'
echo "st=$?"
printf 'echo f\nset +v\necho g\n' > s2; ../sh -v s2
echo "st=$?"
printf 'echo h\n' | ../sh -v
echo "st=$?"
printf 'echo i\necho j' > s3; ../sh -v s3
echo "st=$?"
printf 'echo k; set -v\necho l\nset +v\necho m\n' > s4; ../sh s4
echo "st=$?"
