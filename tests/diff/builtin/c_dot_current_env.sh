echo 'x=from-file; f() { echo func-from-file; }; cd /' > lib
. ./lib; echo "$x $PWD"; f
