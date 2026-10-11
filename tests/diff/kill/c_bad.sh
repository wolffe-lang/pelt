kill -s NOSUCH $$ 2>/dev/null; echo "st=$?"
kill 2>/dev/null; echo "st=$?"
kill -l NOSUCH 2>/dev/null; echo "st=$?"
