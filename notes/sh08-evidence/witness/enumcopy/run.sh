#!/bin/bash
cd "$HOME/lanes/sh08/probe/enumcopy" || exit 9
W=$HOME/lanes/sh08/dev/.wolf-bin/wolf
L=$HOME/lanes/sh08/dev/.wolf-bin/lupin
"$W" --version | head -1
for t in "" --release; do echo "== wolf build $t"; "$W" build $t main.lu -o ec 2>&1; echo "exit=$?"; [ -x ec ] && ./ec; rm -f ec; done
echo "== wolf conform-run --checked"; "$W" conform-run --checked main.lu 2>&1 | tail -3; echo "exit=$?"
echo "== lupin"; "$L" run main.lu 2>&1 | tail -3; echo "exit=$?"
