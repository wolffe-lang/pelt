../sh -ec 'false; echo no'; echo "st=$?"
../sh -uc 'echo ${x-ok}'
../sh -c -e 'false; echo no' 2>/dev/null; echo "st=$?"
../sh -o errexit -c 'false; echo no'; echo "st=$?"
