exec 2>/dev/null
set -v
echo "[$-]"
set +v -a
echo "[$-]"
set -C -f
echo "[$-]"
