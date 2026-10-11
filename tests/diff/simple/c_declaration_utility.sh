x='a b'; HOME=/h
export y=$x; echo "[$y]"
readonly z=$x; echo "[$z]"
export p=~/q:~; echo "$p"
