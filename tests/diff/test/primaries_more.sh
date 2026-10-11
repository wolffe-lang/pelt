# -nt and -ot compare modification times to the nanosecond, and a file
# is not newer than itself; -k is the sticky bit; -ef follows a link;
# -h of a missing name is false; a lone `-t` is a non-empty string.
touch -d 2020-01-01T00:00:00.1 a
touch -d 2020-01-01T00:00:00.9 b
[ b -nt a ]; echo "nt=$?"
[ a -ot b ]; echo "ot=$?"
[ a -nt a ]; echo "self=$?"
mkdir d; chmod 1777 d
[ -k d ]; echo "k=$?"
[ -k a ]; echo "k-plain=$?"
ln -s a l
[ l -ef a ]; echo "ef-link=$?"
[ -h nope ]; echo "h-missing=$?"
[ -t ]; echo "t-alone=$?"
