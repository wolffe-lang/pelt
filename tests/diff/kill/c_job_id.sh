sleep 5 &
kill %1; wait; echo "st=$?"
PATH=/nonexistent; kill -0 $$; echo "builtin=$?"
