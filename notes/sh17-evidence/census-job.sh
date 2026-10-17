#!/bin/bash
# sh17: the script census for base and head, after the head gauntlet
set -u
S=$HOME/lanes/sh17
L=$S/logs
until grep -q ^done $L/head.status 2>/dev/null; do sleep 30; done
$S/census.sh base-unaided $S/sc/pelt-base --build
$S/census.sh base-aided $S/sc/pelt-base --aided
$S/census.sh head-unaided $S/sc/pelt-head
$S/census.sh head-aided $S/sc/pelt-head --aided
echo finished > $L/census.done
