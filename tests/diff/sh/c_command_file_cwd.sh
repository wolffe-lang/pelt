mkdir d; echo 'echo in-path' > d/script; chmod +x d/script; echo 'echo in-cwd' > script
PATH=$PWD/d:$PATH ../sh script
