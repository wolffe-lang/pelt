printf 'echo script-ran $1\n' > s2
chmod +x s2
exec ./s2 arg
echo after
