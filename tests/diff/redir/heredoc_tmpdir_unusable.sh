mkdir ro && chmod a-w ro
TMPDIR=$PWD/ro
big=$(printf '%5000s' x)
cat <<END | wc -c | tr -d ' '
$big
END
echo "program $?"
read -r x <<END
$big
END
echo "read $? ${#x}"
{ wc -c | tr -d ' '; } <<END
$big
END
echo "group $?"
f() { wc -c | tr -d ' '; }
f <<END
$big
END
echo "function $?"
y=$(cat <<END
$big
END
)
echo "substitution $? ${#y}"
cat <<END >out &
$big
END
wait $!
echo "async $?"
wc -c <out | tr -d ' '
eval 'wc -c <<END | tr -d " "
$big
END'
echo "eval $?"
(: <<END
$big
END
echo "special $?")
echo "subshell $?"
