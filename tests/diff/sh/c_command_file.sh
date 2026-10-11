echo 'echo "$0 $# $1"' > script
../sh script a b; ../sh ./script 'x y'
