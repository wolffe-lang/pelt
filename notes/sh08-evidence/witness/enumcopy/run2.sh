#!/bin/bash
cd "$HOME/lanes/sh08/probe/enumcopy" || exit 9
W=$HOME/lanes/sh08/dev/.wolf-bin/wolf
for f in plain.lu; do echo "== $f wolf build"; "$W" build $f -o ec 2>&1; echo "exit=$?"; [ -x ec ] && ./ec; rm -f ec; done
