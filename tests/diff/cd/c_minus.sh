mkdir a b; cd a; cd ../b; cd - | sed 's,.*/,,'; cd - >/dev/null; pwd | sed 's,.*/,,'
