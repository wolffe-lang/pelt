set -C
echo a >f
echo b >f
echo st $?
echo c >|f
cat f
set +C
echo d >f
cat f
