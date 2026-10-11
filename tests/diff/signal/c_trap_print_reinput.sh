trap "echo 'it'\\''s'" INT; trap '' TERM
saved=$(trap); trap - INT TERM
eval "$saved"; trap | sed 's/SIG//' | sort
