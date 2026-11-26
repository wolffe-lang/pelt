# A file without #! that the system will not execute is run as a shell
# script (XCU 2.9.1.4); its redirection is performed once, so under
# set -C the file it created receives the script's output instead of
# being refused as one that exists (pelt#156).
printf 'echo from the script\n' >s
chmod +x s
set -C
./s >f
echo "status $?"
cat f
