# A simple command's own redirection carries its end notice, unlike a
# subshell's redirection (pelt#53). Compare presence, not dash's words.
sh -c 'kill -TERM $$' 2>f
st=$?
if [ -s f ]; then echo "notice in f: $st"; else echo "notice outside: $st"; fi
rm -f f
# A built-in/function name forces the ordinary path too.
f() { :; }
X=1 sh -c 'kill -TERM $$' 2>f
st=$?
if [ -s f ]; then echo "ordinary in f: $st"; else echo "ordinary outside: $st"; fi
rm -f f
