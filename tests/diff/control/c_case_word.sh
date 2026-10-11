touch f1
x='a b'; HOME=/h
case $x in 'a b') echo unsplit;; esac
case f* in f1) echo globbed;; 'f*') echo literal;; esac
case ~ in /h) echo tilde;; esac
case $((1+1))$(echo x) in 2x) echo expanded;; esac
