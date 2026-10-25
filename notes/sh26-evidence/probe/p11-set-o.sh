# item 5 (pelt#17): the option listings, -o notify and ignoreeof among them
set +o
echo ---
set -o
echo ---
set -o ignoreeof; set -o notify; echo "$-"; set +o | grep -E 'ignoreeof|notify'
