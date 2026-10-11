alias hi='echo hello'
printf 'hi 2>/dev/null || echo not-found\n' > s2
../sh ./s2
