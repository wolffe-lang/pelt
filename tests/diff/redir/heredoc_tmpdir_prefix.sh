mkdir ro && chmod a-w ro
big=$(printf '%5000s' x)
TMPDIR=$PWD/ro cat <<END | wc -c | tr -d ' '
$big
END
echo "program $?"
TMPDIR=$PWD/ro read -r x <<END
$big
END
echo "read $? ${#x}"
(TMPDIR=$PWD/ro eval 'wc -c | tr -d " "' <<END
$big
END
echo "eval $?")
echo "subshell $?"
(TMPDIR=$PWD/ro : <<END
$big
END
echo "colon $?")
echo "subshell $?"
