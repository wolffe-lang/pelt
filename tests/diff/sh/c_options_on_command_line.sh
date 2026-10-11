../sh -e -c 'false; echo no'; echo "e=$?"
../sh -u -c 'echo $nope; echo no' 2>/dev/null; echo "u=$?"
../sh -f -c 'echo *'
../sh -ef -c 'case $- in *e*) case $- in *f*) echo ef;; esac;; esac'
../sh -o noglob -c 'echo *'
../sh +e -c 'false; echo plus-e'
../sh -C -c 'echo a > f; echo b > f' 2>/dev/null; cat f
../sh -a -c 'x=1; sh -c "echo \${x-unset}"'
../sh -x -c ': traced' 2>&1 | sed 's/^+* *//'
../sh -n -c 'echo not-run'; echo "n=$?"
