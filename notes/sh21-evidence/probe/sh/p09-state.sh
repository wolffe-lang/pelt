# what the handler sets: kept? exit in it ends what?
command_not_found_handle() { kept=yes; }
nosuch; echo "kept=${kept-no}"
command_not_found_handle() { exit 7; }
nosuch; echo "after exit st=$?"
