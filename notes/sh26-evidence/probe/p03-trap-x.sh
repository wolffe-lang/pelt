# item 4 (pelt#28): a bad option to trap ends a script
trap -x 'echo t' INT
echo "after st=$?"
