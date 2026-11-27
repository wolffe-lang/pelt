export E=1 F=2
unset E
/usr/bin/env > envout; grep -c '^E=' envout
echo "${E-gone} ${F-gone}"
unset F; F=3 /usr/bin/env > envout; grep '^F=' envout
echo "${F-gone}"
echo done
