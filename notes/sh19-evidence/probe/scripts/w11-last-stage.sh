z=0; : | z=1; echo last=$z
w=0; echo x | read w; echo read-last=$w
( env sh -c 'echo $PPID' ) > tmp/pp; read a < tmp/pp; [ "$a" = "$$" ] && echo single-sub-child-parent=shell || echo single-sub-child-parent=other
