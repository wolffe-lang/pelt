unset x
echo [${x+alt}] [${x:+alt}]
x=
echo [${x+alt}] [${x:+alt}]
x=v
echo [${x+alt}] [${x:+alt}]
