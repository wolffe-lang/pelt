# pelt#6, XCU set -v: what is input: a script operand and standard input are written as read, byte for byte (no newline added where the file has none); a -c string never, whether -v is given before it or set inside it (dash; bash writes those too)
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
