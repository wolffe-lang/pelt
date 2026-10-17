f() { :; }
command -v f cd if ls; echo "st=$?"
: > plain; command -v ./plain; echo "plain=$?"; chmod +x plain; command -v ./plain; echo "x=$?"
mkdir d; command -v ./d; echo "d=$?"
mkdir bin; printf '#!/bin/sh\n' > bin/p; chmod +x bin/p; PATH=bin:$PATH; command -v p; echo "rel=$?"
command -v nonexistent-xyz; echo "missing=$?"
command -V nonexistent-xyz >/dev/null 2>&1; echo "V=$?"
command -V cd >/dev/null; echo "Vcd=$?"
