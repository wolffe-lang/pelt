#!/bin/bash
# sh08 baseline at trunk: gauntlet, then the census unaided (building the images) and aided.
set -u
"$HOME/lanes/sh08/gauntlet.sh" base
"$HOME/lanes/sh08/census.sh" base-unaided "$HOME/lanes/sh08/sc/pelt-base" --build
"$HOME/lanes/sh08/census.sh" base-aided "$HOME/lanes/sh08/sc/pelt-base" --aided
echo finished > "$HOME/lanes/sh08/logs/base.done"
