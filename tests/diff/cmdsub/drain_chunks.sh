# Multiple read chunks must survive scratch-region reuse, with the
# substitution's exit status preserved and no bytes lost or aliased.
# Prepare with POSIX awk and start Python only once: Apple's system
# Python startup alone is about 1.8s, so four starts exhaust the budget.
awk 'BEGIN { for(i=0;i<65536;i++) printf "a"; for(i=0;i<65536;i++) printf "b"; printf "c" }' >input-a
awk 'BEGIN { for(i=0;i<65536;i++) printf "c"; for(i=0;i<65536;i++) printf "b"; printf "a" }' >input-b
x=$(cat input-a | cat)
printf '%s' "$x" >captured-a
x=$(cat input-b; exit 7)
st=$?
printf '%s' "$x" >captured-b
python3 -c 'import hashlib
for name in ("captured-a", "captured-b"):
 b=open(name,"rb").read(); print(len(b), hashlib.sha256(b).hexdigest())'
echo status=$st
rm -f input-a input-b captured-a captured-b
