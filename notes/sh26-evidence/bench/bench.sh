#!/bin/bash
# sh26 item 8 (pelt#57, measured only): sh20's bench at the pin, inside
# the container (CPUs 0-3, cpuset and taskset), dash against the pin's
# release and native tiers, nine runs each.
set -u
S=/home/mfwolffe/lanes/sh26
B=$S/bench; rm -rf $B; mkdir -p $B/w; cp $S/pelt-bench/* $B/
cd $B && python3 -I gen-configure-shaped > configure-shaped.sh && sha256sum configure-shaped.sh
python3 -I run --dir $B/w --runs 9 --pin 0-3 dash=/usr/bin/dash release=$S/bin/base/release/pelt native=$S/bin/base/native/pelt
