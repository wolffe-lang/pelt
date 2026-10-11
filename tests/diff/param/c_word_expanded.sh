HOME=/h; unset u; v=val
echo ${u:-~} ${u:-$v} ${u:-$(echo c)} ${u:-$((2+3))} ${u:-`echo b`}
