#!/bin/bash
S=/home/mfwolffe/lanes/sh22
cd $S
PELT_TOOLS=$S/snaps/q3/tools python3 probe/shapes22.py --only ctl-loop,bg-builtin-nowait,bg-program-nowait,script-bg-builtin-nowait bin/pelt-w2-native bin/pelt-w2-release
probe/setm/rss.sh 5000 bin/pelt-w2-release
