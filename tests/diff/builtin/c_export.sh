x=1; export x; sh -c 'echo $x'
export y=2 z=3; sh -c 'echo $y $z'
w=4; export w; w=5; sh -c 'echo $w'
export u; sh -c 'echo ${u-unset}'; u=6; sh -c 'echo $u'
