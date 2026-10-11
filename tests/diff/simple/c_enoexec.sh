printf 'echo "script $# $1"\n' > noshebang; chmod +x noshebang
./noshebang a b; PATH=$PWD:$PATH; noshebang c
