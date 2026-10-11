../sh -v -c 'echo x' 2>&1 >/dev/null | wc -l | tr -d ' '
printf 'echo a\necho b\n' > s; ../sh -v s 2>&1
