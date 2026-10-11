# The signal numbers every host pelt runs on agrees on (4 ILL, 5 TRAP,
# 8 FPE, 11 SEGV, 13 PIPE) are taken as conditions, listed by name and
# reset by number. Recording is all this asks: no such signal is sent.
trap 'echo t' 4 5 8 11 13
echo "set: $?"
trap >listed
sort listed
trap - 4 5 8 11 13
echo "reset: $?"
trap >listed
cat listed
echo done
