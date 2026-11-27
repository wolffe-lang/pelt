i=0
while [ $i -lt 300 ]; do eval "V$i=v$i"; i=$((i+1)); done
i=0
while [ $i -lt 100 ]; do eval "export V$i"; i=$((i+1)); done
i=200
while [ $i -lt 250 ]; do eval "readonly V$i"; i=$((i+1)); done
echo "$V0 $V150 $V299"
V150=new /usr/bin/env > envout; grep '^V150=' envout; grep -c '^V[0-9]*=' envout
echo "V150=$V150"
: $((n=4)) ${m=5}; echo "n=$n m=$m"
V5=five V6=$V5; echo "$V5 $V6"
/usr/bin/env > envout; grep '^V5=' envout
( V210=x; echo unreached ) 2>/dev/null; echo "st=$?"
echo done
