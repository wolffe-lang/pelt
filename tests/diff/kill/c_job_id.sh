sleep 5 &
kill %1 2>/dev/null; wait; echo "st=$?"
PATH=/nonexistent; kill -0 $$; echo "builtin=$?"
