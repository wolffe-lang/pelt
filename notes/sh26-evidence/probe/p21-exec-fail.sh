# item 2: exec's own failures, each in a subshell (exec ends the shell)
(exec ./nope); echo "st=$?"
echo x > f; (exec ./f/x); echo "st=$?"
mkdir d; (exec ./d); echo "st=$?"
echo 'echo hi' > nox; (exec ./nox); echo "st=$?"
ln -s l1 l2; ln -s l2 l1; (exec ./l1); echo "st=$?"
(exec nosuch_sh26); echo "st=$?"
