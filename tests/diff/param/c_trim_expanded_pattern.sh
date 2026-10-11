x=/usr/local/bin; p=/usr; s='*'
echo ${x#$p} ${x#"$p"} ${x##$s/} ${x##"$s"/} ${x%$(echo /bin)}
