# the prompt variables come from the environment when it sets them
PS1='a> ' PS2='b> ' PS4='c ' ../sh -c 'echo "[$PS1][$PS2][$PS4]"'
env -u PS1 -u PS2 -u PS4 ../sh -c 'echo "[$PS1][$PS2][$PS4]"'
