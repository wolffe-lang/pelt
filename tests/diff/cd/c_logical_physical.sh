mkdir -p real/sub; ln -s real/sub link; top=$PWD
cd link; pwd | sed "s,$top,TOP,"; pwd -P | sed "s,$(cd "$top" && pwd -P),TOP,"
cd ..; pwd | sed "s,$top,TOP,"
cd "$top"; cd -P link; pwd | sed "s,$(cd "$top" && pwd -P),TOP,"; cd ..; pwd | sed 's,.*/,,'
cd "$top"; cd -L link; pwd | sed 's,.*/,,'
