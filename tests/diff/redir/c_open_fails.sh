echo x > /nonexistent-dir/f; echo "st=$?"
cat < /nonexistent-file; echo "st=$?"
mkdir d; echo y > d; echo "st=$?"
