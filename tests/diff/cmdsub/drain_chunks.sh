# Multiple read chunks must survive scratch-region reuse, with the
# substitution's exit status preserved and no bytes lost or aliased.
x=$(python3 -c 'import os; os.write(1, b"a"*65536 + b"b"*65536 + b"c")' | cat)
printf '%s' "$x" | python3 -c 'import sys,hashlib; b=sys.stdin.buffer.read(); print(len(b), hashlib.sha256(b).hexdigest())'
x=$(python3 -c 'import os; os.write(1, b"c"*65536 + b"b"*65536 + b"a")'; exit 7)
st=$?
printf '%s' "$x" | python3 -c 'import sys,hashlib; b=sys.stdin.buffer.read(); print(len(b), hashlib.sha256(b).hexdigest())'
echo status=$st
