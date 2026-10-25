# pelt#6, XCU set -v: a script's input written to standard error as it is read, compared byte for byte (standard error is standard output here): every line of a compound command, comments and blank lines, a here-document's body, a function's definition, a sourced file's lines; never an eval string; the set +v line itself is input read while -v was on
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
