trap 'echo a' INT
trap '' TERM
trap 'echo x' EXIT
trap 'echo h' HUP
trap
