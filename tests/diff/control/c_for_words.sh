touch f1 f2
x='a b'
for i in $x "$x" f* $(echo c d) ; do echo "[$i]"; done; echo "last=$i"
