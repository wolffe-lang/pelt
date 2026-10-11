x=/one/two/three
echo ${x#*/} ${x##*/} ${x#/one} ${x#} ${x##} ${x#z} ${x#?} ${x##/*/}
