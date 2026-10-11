for i in 1 2 3; do eval 'continue'; echo no; done; echo loop-done
for i in 1 2 3; do eval 'break'; done; echo "i=$i"
f() { eval 'return 5'; echo no; }; f; echo $?
