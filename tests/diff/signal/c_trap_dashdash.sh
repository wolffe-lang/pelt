trap -- 'echo x' INT; trap | sed 's/SIG//'
trap -- - INT; trap | wc -l | tr -d ' '
