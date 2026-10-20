# pelt#42: command_not_found_handle is an interactive shell's: a script, a
# -c string and a script on standard input define it and still say
# not found, 127
command_not_found_handle() { echo "handler: $1"; return 0; }
nosuch a 2>/dev/null; echo "script st=$?"
../sh -c 'command_not_found_handle() { echo "handler: $1"; }; nosuch b 2>/dev/null; echo "-c st=$?"'
echo 'command_not_found_handle() { echo "handler: $1"; }; nosuch c 2>/dev/null; echo "stdin st=$?"' | ../sh
