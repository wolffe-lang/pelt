alias echo='echo x'
echo y
alias a=b b=a
a 2>/dev/null; echo "st=$?"
