mkdir real
ln -s real link
cd link
echo "${PWD##*/}"
cd -P .
echo "${PWD##*/}"
cd ..
cd -L link
cd ..
echo "${PWD##*/}"
