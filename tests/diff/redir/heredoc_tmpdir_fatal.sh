mkdir ro && chmod a-w ro
big=$(printf '%5000s' x)
TMPDIR=$PWD/ro : <<END
$big
END
echo "colon: $?"
