(ulimit -f 1; trap '' XFSZ 2>/dev/null; dd if=/dev/zero of=big bs=1024 count=8 2>/dev/null; echo "dd=$?" | sed 's/dd=[1-9][0-9]*/dd=failed/')
ls -l big 2>/dev/null | wc -l | tr -d ' '
