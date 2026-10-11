mkdir real; ln -s real link; top=$PWD; cd link
pwd | sed "s,$top,TOP,"; pwd -L | sed "s,$top,TOP,"; pwd -P | sed "s,.*/,,"
pwd -L -P | sed 's,.*/,,'; pwd -P -L | sed 's,.*/,,'
