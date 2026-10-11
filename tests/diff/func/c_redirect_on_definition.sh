f() { echo to-file; } > out
ls; f; f; cat out
n=1; g() { echo x; } > "g$n"; n=2; g; ls
