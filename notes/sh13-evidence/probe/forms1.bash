[0] -> st=0 now=0000
[7777] -> st=0 now=0777
[1777] -> st=0 now=0777
[0777] -> st=0 now=0777
[777] -> st=0 now=0777
[8] -> st=1 now=0022
[00022] -> st=0 now=0022
[000000022] -> st=0 now=0022
[] -> st=1 now=0022
[0o22] -> st=1 now=0022
[22x] -> st=1 now=0022
[-022] -> st=2 now=0022
[+022] -> st=1 now=0022
dashdash st=0 0027
S-with-op st=0 out=[u=rwx,g=rx,o=] now=0022
bad-opt st=2
two-ops st=0 now=0027
u=rwx,g=rx,o=rx
SS st=0
0022
dd-only st=0
u=rwx,g=rx,o=rx
S-dd st=0
[+w] -> st=0 now=0005 S=u=rwx,g=rwx,o=w
[-w] -> st=2 now=0027 S=u=rwx,g=rx,o=
[=r] -> st=0 now=0333 S=u=r,g=r,o=r
[a=] -> st=0 now=0777 S=u=,g=,o=
[u=g] -> st=0 now=0227 S=u=rx,g=rx,o=
[g=u-w] -> st=0 now=0027 S=u=rwx,g=rx,o=
[o+X] -> st=0 now=0026 S=u=rwx,g=rx,o=x
[u+s] -> st=0 now=0027 S=u=rwx,g=rx,o=
[+t] -> st=0 now=0027 S=u=rwx,g=rx,o=
[g+t] -> st=0 now=0027 S=u=rwx,g=rx,o=
[u=rwx,g=rx,o=] -> st=0 now=0027 S=u=rwx,g=rx,o=
[ug+rw] -> st=0 now=0007 S=u=rwx,g=rwx,o=
[a-rwx] -> st=0 now=0777 S=u=,g=,o=
[u=r,u+w] -> st=0 now=0127 S=u=rw,g=rx,o=
[u=rwx,,o=r] -> st=1 now=0027 S=u=rwx,g=rx,o=
[u] -> st=1 now=0027 S=u=rwx,g=rx,o=
[=r] -> st=0 now=0333 S=u=r,g=r,o=r
[u=rwx,] -> st=1 now=0027 S=u=rwx,g=rx,o=
[,u=rwx] -> st=1 now=0027 S=u=rwx,g=rx,o=
[u=rw,g=u] -> st=0 now=0107 S=u=rw,g=rwx,o=
[g=o] -> st=0 now=0077 S=u=rwx,g=,o=
[go=u] -> st=0 now=0000 S=u=rwx,g=rwx,o=rwx
[u+x,g-x] -> st=0 now=0037 S=u=rwx,g=r,o=
[a+X] -> st=0 now=0026 S=u=rwx,g=rx,o=x
[u=rwxs] -> st=0 now=0027 S=u=rwx,g=rx,o=
[o=t] -> st=0 now=0027 S=u=rwx,g=rx,o=
[au=r] -> st=0 now=0333 S=u=r,g=r,o=r
[u+r+w] -> st=0 now=0027 S=u=rwx,g=rx,o=
[u+r-w] -> st=0 now=0227 S=u=rx,g=rx,o=
[u=+r] -> st=0 now=0327 S=u=r,g=rx,o=
[u==r] -> st=0 now=0327 S=u=r,g=rx,o=
[g+u] -> st=0 now=0007 S=u=rwx,g=rwx,o=
[u=r g=r] -> st=1 now=0027 S=u=rwx,g=rx,o=
[U=r] -> st=1 now=0027 S=u=rwx,g=rx,o=
[u=X] -> st=0 now=0627 S=u=x,g=rx,o=
[u+X] -> st=0 now=0027 S=u=rwx,g=rx,o=
[ugoa-x] -> st=0 now=0137 S=u=rw,g=r,o=
exit=0
