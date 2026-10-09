mkdir sub
cd sub
p=$(/bin/pwd)
echo "${p##*/}"
