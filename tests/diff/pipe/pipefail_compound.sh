set -o pipefail
while false | true; do echo in; break; done; echo done
x=$(false | true); echo "cmdsub $?"
false | true & wait $!; echo "bg $?"
{ false; } | { true; }; echo "braces $?"
for i in 1; do false; done | cat; echo "loop $?"
