# A condition's name is taken in any case and without `SIG` (XCU `trap`
# makes the prefix an extension; dash does not take it), and is listed
# in upper case.
trap 'echo x' hup Int quIT
trap
trap - HUP int QUIT
trap 'echo y' SIGHUP 2>/dev/null; echo "sig-prefix=$?"
trap 'echo y' NOSUCH 2>/dev/null; echo "unknown=$?"
trap 'echo y' USR1 NOSUCH USR2 2>/dev/null; echo "mixed=$?"
trap | sort
trap - USR1 USR2
trap 'echo z' exit
trap
