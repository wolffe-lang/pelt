echo data > f
exec 4<f; cat <&4; exec 4<&-; exec 4<&-; echo "st=$?"
exec 5<f; read a 0<&5; echo "$a"
