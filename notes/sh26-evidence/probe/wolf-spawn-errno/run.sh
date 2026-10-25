#!/bin/bash
# sh26: build the spawn probe with the pinned wolf and run it on each reason
set -u
S=/home/mfwolffe/lanes/sh26
W=$S/pelt/.wolf-bin/wolf
D=$S/tmp/spawnprobe; rm -rf $D; mkdir -p $D/w; cp $S/probe/wolf-spawn-errno/main.lu $D/
cd $D && WOLF_STD=$S/pelt/.wolf-bin/std $W build --std-root $S/pelt/.wolf-bin/std main.lu -o probe 2>&1 | tail -3
cd $D/w
echo x > f; ln -s loop1 loop2; ln -s loop2 loop1; ln -s nowhere dangle; mkdir dd; echo 'echo hi' > nox
printf '#!/bin/sh\necho ran\n' > busy; chmod +x busy; exec 5>>busy
printf '#!/nonexistent/interp\n' > badi; chmod +x badi
printf '\0\0binary\n' > bin; chmod +x bin
mkdir -p locked/sub; chmod 0 locked
../probe ./nope ./f/x ./loop1 ./dangle ./$(printf '%0300d' 0) ./dd ./nox ./busy ./badi ./bin ./locked/sub
chmod 755 locked
