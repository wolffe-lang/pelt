# What `kill` refuses, each with status 2 and nothing sent: a `SIG`
# prefix (an extension dash does not have), EXIT, a word that is no
# signal, `--` after `-name`, a missing operand.
sleep 5 & p=$!
for how in '-s SIGTERM' '-SIGTERM' '-s EXIT' '-EXIT' '-s 1x' '-1x' '-s -1' '-x' '-TERM --' '-- -TERM' '-s NOSUCH' '-s'; do
  kill $how $p 2>/dev/null; echo "[$how] $?"
done
kill 2>/dev/null; echo "none=$?"
kill -s TERM 2>/dev/null; echo "no-pid=$?"
kill -9 2>/dev/null; echo "no-pid-9=$?"
kill -- 2>/dev/null; echo "dashdash-only=$?"
kill -0 $p; echo "still-there=$?"
kill $p; wait $p 2>/dev/null; echo "ended=$(kill -l $?)"
kill %9 2>/dev/null; echo "no-such-job=$?"
kill %nosuch 2>/dev/null; echo "no-such-name=$?"
