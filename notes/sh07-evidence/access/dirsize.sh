# Whether an empty directory "has a size" (test -s) is the
# filesystem's answer, not the shell's: witness.sh runs this under dash
# on a tmpfs and on the container's own filesystem.
mkdir d
if [ -s d ]; then echo "-s empty dir: true"; else echo "-s empty dir: false"; fi
