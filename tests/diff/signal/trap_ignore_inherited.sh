trap '' TERM
/bin/sh -c 'kill -TERM $$; echo child-alive'
echo $?
