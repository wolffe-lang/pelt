# what the handler sets: kept? exit in it ends what?
function fish_command_not_found; set -g kept yes; end
nosuch; echo "kept=$kept"
function fish_command_not_found; exit 7; end
nosuch; echo "after exit st=$status"
