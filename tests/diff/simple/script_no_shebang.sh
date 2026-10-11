printf 'echo ran $1\n' > s2
chmod +x s2
./s2 a
echo st=$?
