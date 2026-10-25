# item 2 (pelt#61): a slashed path that does not exist, a directory, a
# file with no x bit, and a plain name found nowhere
../nonexistent/x; echo "st=$?"
./nope; echo "st=$?"
mkdir d; ./d; echo "st=$?"
echo 'echo hi' > nox; ./nox; echo "st=$?"
nosuchcmd_sh26; echo "st=$?"
