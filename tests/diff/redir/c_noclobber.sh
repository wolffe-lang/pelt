set -C
echo a > f; echo b > f; echo "st=$?"; cat f
echo c >| f; cat f
echo d > /dev/null; echo "devnull=$?"
ln -s f lnk; echo e > lnk; echo "link=$?"; cat f
set +C; echo g > f; cat f
