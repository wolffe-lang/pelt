# item 3 (pelt#6): set -v granularity, standard error shown with stdout
exec 2>&1
set -v
echo one   # a comment
# a comment line

echo two; echo three
if true
then
  echo four
fi
cat <<EOF
body $HOME
EOF
f() {
  echo in-f
}
f
eval 'echo ev'
echo 'echo dotted' > d.sh; . ./d.sh
x=$(echo sub
)
set +v
echo quiet
