FOO=bar ../sh -c 'echo "$FOO"; FOO=baz; env | grep "^FOO="'
