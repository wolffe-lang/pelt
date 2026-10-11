SH=$PWD/../sh
mkdir real; ln -s real link; cd link
$SH -c 'echo "$PWD"' | sed 's,.*/,,'
PWD=/nonsense $SH -c 'echo "$PWD"' | sed 's,.*/,,'
