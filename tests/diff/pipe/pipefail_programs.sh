set -o pipefail
../sh -c 'exit 2' | cat; echo $?
cat ./nonexistent 2>/dev/null | cat; echo $?
yes | head -n 1 >/dev/null; echo $?
printf 'a\n' | grep -q b | cat; echo $?
