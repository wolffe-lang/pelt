mkdir -p a/b; top=$PWD
cd a/./b//; pwd | sed "s,$top,TOP,"
cd ../../a/b/..; pwd | sed "s,$top,TOP,"
cd //; pwd | sed 's,^//*$,/,'
