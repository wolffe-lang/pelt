cd /; cd bin; pwd; echo "PWD=$PWD"
cd //; pwd
cd //bin; pwd
cd //; cd bin; pwd
cd /; CDPATH=/; cd bin; pwd; unset CDPATH
cd /; cd ./bin; pwd
cd /; cd bin/; pwd
cd /usr/; cd bin; pwd
