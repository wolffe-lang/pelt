printf 'one\ntwo\nthree\n' > f
{ read a; read b; cat; } < f; echo "$a $b"
{ read a; head -n 1; } < f
