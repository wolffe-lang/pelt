mkdir d; echo 'echo found-in-path' > d/lib
PATH=$PWD/d:$PATH; . lib
echo 'echo in-cwd' > lib2; (. lib2) 2>/dev/null; echo "st=$?"
