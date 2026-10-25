# item 5 (pelt#17): trap -p (a special built-in: in a subshell, so its
# error ends only that), PS4, set -x forms, -o notify
trap 'echo i' INT
(trap -p INT; echo "trap-p st=$?"); echo "sub st=$?"
trap; echo "trap st=$?"
x=tag
PS4='$x> '
set -x
echo traced
set +x
PS4='+ '
set -x
y=1
y=2 true
z='a b' w=$z
echo "$z" $z 'q"t' "it's" a\ b '' "" \$x
for i in 1; do :; done
case a in a) : ;; esac
[ a = a ]
f() { :; }; f arg
v=$(echo sub)
: "$(echo inner)"
echo hi >/dev/null 2>&1
x=1 >/dev/null
{ echo brace; } >/dev/null
while false; do :; done
if true; then :; fi
! true
true && false || true
echo a | cat >/dev/null
set +x
set -o notify; echo "notify st=$?"; case $- in *b*) echo b-in-flags;; esac
set +o | grep -E 'notify|ignoreeof|verbose|xtrace'
