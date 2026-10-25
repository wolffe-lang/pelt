# item 2 (pelt#63): a #!-less executable text file and a binary garbage one
printf 'echo "script ran: $0 $1"\nexit 3\n' > t; chmod +x t
./t arg; echo "st=$?"
printf '\0\0\0\0binary\n' > bin; chmod +x bin
./bin; echo "st=$?"
printf '\177ELF\2\1\1garbage\n' > elf; chmod +x elf
./elf; echo "st=$?"
printf 'x\0y\necho after\n' > nul2; chmod +x nul2
./nul2; echo "st=$?"
printf '\nfoo\0\n' > late; chmod +x late
./late; echo "st=$?"
(exec ./t a2); echo "exec st=$?"
