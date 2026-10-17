h() { printf '%s' "$1" | od -An -tx1 | tr -d ' \n'; echo; }
h $'\E\?\q\z\8'
h $'\x414'
h $'a\xgb'
h $'\0101\400x'
h $'\ca\c?\c\\'
h $'ab\0cd'
h $'ab\x00cd'x
h $'é€'
h $'\U000000e9'
h $'a\u'
