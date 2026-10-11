trap 'echo x' 0; trap | sed 's/SIG//'; trap - 0
trap ':' HUP 2 QUIT 15; trap | sed 's/SIG//' | sort; trap - 1 INT 3 TERM
trap ':' KILL 2>/dev/null; echo "kill=$?"
