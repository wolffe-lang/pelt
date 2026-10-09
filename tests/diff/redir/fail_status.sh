cat <nosuch_file
echo st $?
{ :; } <nosuch
echo st $?
f() { :; }
f <nosuch
echo st $?
