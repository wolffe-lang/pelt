# the hash table after a miss handled
command_not_found_handle() { return 0; }
nosuch; hash 2>&1 | grep -c nosuch
