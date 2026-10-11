printf '\0\0\0\0binary\n' > bin; chmod +x bin
./bin 2>/dev/null; echo "st=$?"
