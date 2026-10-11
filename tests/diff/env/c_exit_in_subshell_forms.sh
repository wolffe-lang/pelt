( exit 1 ); : $(exit 2); exit 3 | :; { exit 4; } & wait
echo survived
