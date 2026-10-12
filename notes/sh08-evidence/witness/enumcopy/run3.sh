#!/bin/bash
cd "$HOME/lanes/sh08/probe/enumcopy" || exit 9
W=$HOME/lanes/sh08/dev/.wolf-bin/wolf
L=$HOME/lanes/sh08/dev/.wolf-bin/lupin
for t in "" --release; do echo "== wolf build $t min.lu"; "$W" build $t min.lu -o ec 2>&1; echo "exit=$?"; [ -x ec ] && ./ec; rm -f ec; done
echo "== conform-run --checked"; "$W" conform-run --checked min.lu 2>&1 | grep -o '"verdict":"[^"]*"\|"stdout_inline":"[^"]*"'
echo "== lupin"; "$L" run min.lu; echo "exit=$?"
