W=$PWD
mkdir sub
set -x
sub
set +x
echo "trace ${PWD#$W}"
cd "$W"
