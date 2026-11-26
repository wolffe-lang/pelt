# A built-in that reports an error still has its redirection performed
# once: under set -C printf writes what it can convert into the file it
# created, and its own status follows (XCU printf; 2.9.1; pelt#156).
set -C
printf '%d\n' abc >f
echo "status $?"
cat f
