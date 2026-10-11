mkdir -p base/target target; top=$PWD
CDPATH=$top/base; cd target | sed "s,$top,TOP,"; cd target >/dev/null; pwd | sed "s,$top,TOP,"
cd "$top"; cd ./target; pwd | sed "s,$top,TOP,"
cd "$top"; CDPATH=:$top/base; cd target; pwd | sed "s,$top,TOP,"
