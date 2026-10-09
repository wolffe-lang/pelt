mkdir -p a/b
cd a/b
cd ..
echo "${PWD##*/}"
cd ./b
echo "${PWD##*/}"
