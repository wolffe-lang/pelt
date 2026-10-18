#!/bin/bash
# sh18: the script census for the bare pin and the head, after the head gauntlet
set -u
S=$HOME/lanes/sh18
L=$S/logs
H=${1:-head3}
until grep -q ^done $L/$H.status 2>/dev/null; do sleep 30; done
$S/census.sh pin-unaided $S/sc/pelt-pin --build
$S/census.sh pin-aided $S/sc/pelt-pin --aided
$S/census.sh head-unaided $S/sc/pelt-$H
$S/census.sh head-aided $S/sc/pelt-$H --aided
echo finished > $L/census.done
