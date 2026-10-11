echo $$ > p
exec /bin/sh -c 'echo $$ > q; cmp -s p q && echo same'
