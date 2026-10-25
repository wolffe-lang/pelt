# item 2 (pelt#63): which shell runs a #!-less executable text file, on
# the plain path and after exec: the file names its interpreter
printf 'echo "0=$0 1=$1 bash=${BASH_VERSION:+yes}"\n' > who; chmod +x who
./who a; echo "plain st=$?"
(exec ./who b); echo "exec st=$?"
PATH=$PWD:$PATH; who c; echo "path st=$?"
