# The operands: a process id (blanks and a plus sign before it are
# taken), several of them, one that names no process (status 1), a word
# that is no number (status 2).
kill -0 $$; echo "self=$?"
kill -s 0 $$; echo "self-s0=$?"
kill -0 "+$$"; echo "plus=$?"
kill -0 " $$"; echo "blank=$?"
kill -0 abc 2>/dev/null; echo "word=$?"
kill -0 12x 2>/dev/null; echo "mixed=$?"
kill -0 '' 2>/dev/null; echo "empty=$?"
kill -0 99999999999999999999 2>/dev/null; echo "huge=$?"
sleep 5 & a=$!; sleep 5 & b=$!
kill -0 $a $b; echo "two=$?"
kill $a $b; wait $a 2>/dev/null; wait $b 2>/dev/null
kill -0 $a 2>/dev/null; echo "gone=$?"
kill $a 2>/dev/null; echo "gone-term=$?"
sleep 5 & c=$!
kill -0 $a $c 2>/dev/null; echo "one-gone=$?"
kill $c; wait $c 2>/dev/null; echo "ended=$(kill -l $?)"
