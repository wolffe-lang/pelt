f() { :; }; alias a='echo x'
command -v ls | sed 's,.*/,/,'
command -v f; command -v cd; command -v :; command -v if; command -v a
command -v nonexistent-xyz; echo "st=$?"
command -v ./nonexistent; echo "st=$?"
: > plain; command -v ./plain; echo "st=$?"
chmod +x plain; command -v ./plain
