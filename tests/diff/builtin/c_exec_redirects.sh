exec 3>f; echo a >&3; exec 3>&-; cat f
exec > out; echo to-out; exec >&2; cat out >&2
