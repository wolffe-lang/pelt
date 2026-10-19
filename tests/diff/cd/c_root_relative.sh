# pelt#37: a relative cd from / joins without a second slash (dash, bash)
cd /; cd bin; pwd; echo "$PWD"
cd /; cd ./bin; pwd
cd /; cd bin/; pwd
