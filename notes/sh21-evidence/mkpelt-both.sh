#!/bin/bash
# sh21: trunk be1a75d first (sh19 cd05c3b's digest expected: no src/ change since), then the last src/ commit
cd $HOME/lanes/sh21
./mkpelt-job.sh be1a75da02554a80fe2545feb899fbcce904eb07 trunk
./mkpelt-job.sh 6bf7d2a$(git -C pelt rev-parse 6bf7d2a | cut -c8-) head
echo both-done
