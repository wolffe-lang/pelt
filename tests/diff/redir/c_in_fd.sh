echo data > f
cat <f; cat 0<f; exec 5<f; cat <&5; exec 5<&-
